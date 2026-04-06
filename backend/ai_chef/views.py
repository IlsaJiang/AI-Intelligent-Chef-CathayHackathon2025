import logging
import os
import socket

import dashscope
from django.conf import settings
from menu.models import Dish, Allergen
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AIChefChatMessage
from surveys.models import MilesTransaction

logger = logging.getLogger(__name__)


class AIChefChatView(APIView):
    permission_classes = [AllowAny]  # 允许未登录用户使用，但只有登录用户才能获得奖励
    
    def post(self, request):
        user_query = request.data.get("message", "")
        user_language = request.data.get("language", "zh-HK")  # 获取用户语言偏好
        if not user_query:
            return Response({"error": "Empty message", "detail": "消息内容不能为空"}, status=400)

        original_getaddrinfo = socket.getaddrinfo

        # 🔧 修复 DNS 解析问题 - 手动设置域名到 IP 的映射
        def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            if host == "dashscope.aliyuncs.com":
                # 使用阿里云的 IP 地址
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('39.96.182.163', port))]
            return original_getaddrinfo(host, port, family, type, proto, flags)
        
        socket.getaddrinfo = custom_getaddrinfo

        try:
            # ✅ 获取 API key
            api_key = getattr(settings, "DASHSCOPE_API_KEY", os.getenv("DASHSCOPE_API_KEY"))
            if not api_key:
                logger.error("DASHSCOPE_API_KEY is not configured")
                return Response({
                    "error": "AI服务配置错误",
                    "detail": "服务器未配置AI服务密钥，请联系管理员"
                }, status=500)

            dashscope.api_key = api_key  # ✅ 手动注入

            menu_context = self._build_menu_context(user_language)
            prompt = self._build_prompt(user_language, user_query, menu_context)

            response = dashscope.Generation.call(
                model="qwen-plus",
                prompt=prompt,
                max_tokens=200,
                temperature=0.7,
                top_p=0.8,
            )

            logger.info(f"DashScope response type: {type(response)}")
            logger.info(f"DashScope response: {response}")

            reply_text = self._extract_reply_text(response)
            if not reply_text:
                reply_text = self._default_reply(user_query)

            response_data = {"reply": reply_text}

            # 只有登录用户才记录对话和发放奖励
            if request.user and request.user.is_authenticated:
                try:
                    chat_message = AIChefChatMessage.objects.create(
                        user=request.user,
                        message=user_query,
                        reply=reply_text
                    )

                    reward_data = self._check_and_award_reward(request.user, chat_message)
                    if reward_data:
                        response_data["reward"] = reward_data
                except Exception as db_error:
                    logger.error(f"Failed to save chat message or check reward: {db_error}")

            return Response(response_data)

        except Exception as e:
            import traceback
            logger.error("=== AI 主廚接口發生異常 ===")
            logger.error(traceback.format_exc())

            fallback_reply = self._build_error_reply(user_query, str(e))

            response_data = {"reply": fallback_reply}

            if request.user and request.user.is_authenticated:
                try:
                    AIChefChatMessage.objects.create(
                        user=request.user,
                        message=user_query,
                        reply=fallback_reply
                    )
                except Exception as db_error:
                    logger.error(f"Failed to save chat message: {db_error}")

            return Response(response_data)

        finally:
            socket.getaddrinfo = original_getaddrinfo
    
    def _check_and_award_reward(self, user, current_message):
        """检查用户的对话次数，每3次对话奖励100里数"""
        # 统计用户的所有对话记录（包括刚刚创建的这条）
        total_messages = AIChefChatMessage.objects.filter(user=user).count()
        
        # 每3次对话奖励一次（第3、6、9...次）
        if total_messages % 3 == 0 and total_messages > 0:
            # 检查本次对话是否已经奖励过（避免重复奖励）
            # 查找本次对话时间之前最近的奖励记录
            # 如果最近的奖励是在本次对话之前，且奖励次数 < total_messages / 3，则需要发放奖励
            reward_count = MilesTransaction.objects.filter(
                user=user,
                reason='ai_chef_chat'
            ).count()
            
            expected_reward_count = total_messages // 3
            
            # 如果奖励次数少于预期，则发放奖励
            if reward_count < expected_reward_count:
                # 发放100里数奖励
                MilesTransaction.objects.create(
                    user=user,
                    miles=100,
                    description=f'AI厨师对话奖励（第{total_messages}次对话）',
                    reason='ai_chef_chat'
                )
                
                return {
                    'miles': 100,
                    'points': 0,
                    'reason': 'ai_chef_chat',
                    'message': f'恭喜！您已完成{total_messages}次对话，获得100里数奖励！'
                }
        
        return None

    def _build_menu_context(self, user_language: str) -> str:
        dishes = Dish.objects.all().prefetch_related('allergens')
        if not dishes.exists():
            return ""

        header_map = {
            'en': "\n\n【Menu Highlights】\n",
            'zh': "\n\n【我们的菜单】\n",
            'zh-HK': "\n\n【我們的菜單】\n",
        }
        menu_context = header_map.get(user_language, header_map['zh-HK'])

        for dish in dishes:
            allergens_zh = ", ".join([a.name_zh for a in dish.allergens.all() if a.name_zh]) or '无'
            allergens_en = ", ".join([a.name_en for a in dish.allergens.all() if a.name_en]) or 'None'

            if user_language == 'en':
                dish_name = dish.name_en or dish.name_zh or "Unknown Dish"
                dish_desc = (dish.desc_en or dish.desc_zh or "").strip()
                allergen_label = "Allergens"
                allergens_text = allergens_en
            elif user_language == 'zh':
                dish_name = dish.name_zh or dish.name_en or "未知菜品"
                dish_desc = (dish.desc_zh or dish.desc_en or "").strip()
                allergen_label = "过敏原"
                allergens_text = allergens_zh
            else:  # zh-HK / default
                name_zh_hk = getattr(dish, 'name_zh_hk', None)
                desc_zh_hk = getattr(dish, 'desc_zh_hk', None)
                dish_name = name_zh_hk or dish.name_zh or dish.name_en or "未知菜品"
                dish_desc = (desc_zh_hk or dish.desc_zh or dish.desc_en or "").strip()
                allergen_label = "過敏原"
                allergens_text = allergens_zh if allergens_zh != '无' else '無'

            dish_desc = (dish_desc[:500] + "...") if len(dish_desc) > 500 else dish_desc

            menu_context += f"""
━━━━━━━━━━━━━━━━━━━━
菜品名称：{dish_name}
热量：{dish.calories if dish.calories else '未提供'}千卡
蛋白质：{dish.protein_g if dish.protein_g else '未提供'}克
脂肪：{dish.fat_g if dish.fat_g else '未提供'}克
碳水化合物：{dish.carbs_g if dish.carbs_g else '未提供'}克
{allergen_label}：{allergens_text}

详细介绍：
{dish_desc}
"""

        return menu_context

    def _build_prompt(self, user_language: str, user_query: str, menu_context: str) -> str:
        concise_rules_cn = """
【重要规则】
1. 只回答以下菜单中出现的菜品或饮品
2. 若问题不在菜单范围，请礼貌说明并推荐相似菜品
3. 所有营养、食材、过敏原信息必须严格基于菜单
4. 缺失信息需直接说明“暂未提供”
5. 使用要点式、100字以内、语气友好
"""

        concise_rules_en = """
[IMPORTANT RULES]
1. ONLY answer about dishes/beverages listed below
2. If the request is outside the menu, politely decline and suggest similar items
3. Nutrition, ingredients, allergens must follow the menu precisely
4. If information is missing, say “this information is not currently available”
5. Keep it under 100 words in a friendly bullet style
"""

        if user_language == 'en':
            return (
                'You are a virtual chef named "Cathay AI Chef", knowledgeable about Chinese cuisine and airline dining culture.\n'
                'Your tone should be warm, professional, and culturally rich.\n'
                f"{concise_rules_en}\n"
                f"{menu_context}\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"Passenger question: \"{user_query}\"\n"
                "Answer in English with concise bullet-style highlights."
            )
        elif user_language == 'zh':
            return (
                "你是一位名叫「国泰AI主厨」的虚拟厨师，精通中华料理与航空餐文化。\n"
                "请用温和、专业的语气回答。\n"
                f"{concise_rules_cn}\n"
                f"{menu_context}\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"乘客提问：「{user_query}」\n"
                "请用简体中文、要点式地回答。"
            )
        else:
            rules_tc = concise_rules_cn.replace('暂未提供', '暫未提供').replace('简体', '繁體')
            return (
                "你是一位名叫「國泰AI主廚」的虛擬廚師，熟悉中華料理與航空餐文化。\n"
                "請保持溫和、專業且具文化底蘊的語氣。\n"
                f"{rules_tc}\n"
                f"{menu_context}\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"乘客提問：「{user_query}」\n"
                "請用繁體中文、重點式地回覆。"
            )

    def _extract_reply_text(self, response):
        reply_text = None

        if isinstance(response, dict):
            output = response.get('output')
            if isinstance(output, dict):
                reply_text = output.get('text')
                if not reply_text and output.get('choices'):
                    choice = output['choices'][0]
                    if isinstance(choice, dict):
                        message = choice.get('message', {})
                        reply_text = message.get('content') or choice.get('text')
            elif response.get('text'):
                reply_text = response.get('text')

        if not reply_text and hasattr(response, 'output'):
            output = getattr(response, 'output', None)
            if isinstance(output, dict):
                reply_text = output.get('text')
                if not reply_text and output.get('choices'):
                    choice = output['choices'][0]
                    if isinstance(choice, dict):
                        message = choice.get('message', {})
                        reply_text = message.get('content') or choice.get('text')
            elif isinstance(output, str):
                reply_text = output

        if not reply_text and hasattr(response, 'text'):
            reply_text = getattr(response, 'text', None)

        return reply_text.strip() if reply_text else None

    def _default_reply(self, user_query: str) -> str:
        return (
            f"您好！关于「{user_query}」，作为国泰AI主厨，我很乐意分享更多信息，"
            "不过目前AI服务暂时无法提供结果，请稍后再试或联系客服。"
        )

    def _build_error_reply(self, user_query: str, error_message: str) -> str:
        lower_msg = error_message.lower()
        if any(keyword in lower_msg for keyword in ["api_key", "authentication"]):
            return "抱歉，AI服务暂时不可用，可能是配置问题，请稍后再试。"
        if any(keyword in lower_msg for keyword in ["network", "connection"]):
            return "抱歉，目前无法连接到AI服务，请检查网络后再试。"
        if any(keyword in lower_msg for keyword in ["quota", "limit"]):
            return "抱歉，AI服务调用次数已用尽，请稍后再试。"
        return self._default_reply(user_query)