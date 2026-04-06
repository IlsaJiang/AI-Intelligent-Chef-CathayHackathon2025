from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.utils import timezone
from .models import SurveyResponse, LeftoverSubmission, PointTransaction, PeriodicFeedback
from rest_framework import serializers
from menu.models import Dish
from menu.serializers import DishSerializer

class SurveyResponseSerializer(serializers.ModelSerializer):
    dish_detail = DishSerializer(source='dish', read_only=True)
    
    class Meta:
        model = SurveyResponse
        fields = '__all__'

class LeftoverSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeftoverSubmission
        fields = '__all__'

class PointTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointTransaction
        fields = '__all__'

class PeriodicFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicFeedback
        fields = '__all__'

class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all().order_by('-created_at')  # type: ignore
    serializer_class = SurveyResponseSerializer

    def create(self, request, *args, **kwargs):
        # 创建问卷响应
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 保存问卷响应
        survey_response = serializer.save()
        
        # 检查是否应该发放里数（首次提交且用户已登录）
        user = request.user if request.user.is_authenticated else None
        
        # 发放里数逻辑
        if survey_response.dish:
            # 检查该用户是否已经对该菜品提交过评价并获得过里数
            existing_filter = SurveyResponse.objects.filter(
                dish=survey_response.dish, 
                miles_awarded=True
            )
            
            # 如果用户已认证，添加用户过滤
            if user:
                existing_filter = existing_filter.filter(user=user)
            # 如果用户未认证，根据IP地址或其他标识来判断（简化处理）
            # 暂时允许未认证用户也能获得里数，但防止重复
            
            existing_awarded = existing_filter.exists()
            
            # 即使是未认证用户，也应该能获得里数（但只能获得一次）
            if not existing_awarded:
                # 发放里数（例如：每次评价获得10里数）
                miles_to_award = 10
                
                # 更新问卷响应记录
                survey_response.miles_awarded = True
                survey_response.awarded_at = timezone.now()
                survey_response.save()
                
                # 创建里数记录
                PointTransaction.objects.create(
                    user=user,
                    survey=survey_response,
                    miles=miles_to_award,
                    description=f"评价菜品 {survey_response.dish.name_zh} 获得里数"
                )
                
                return Response({
                    'survey': serializer.data,
                    'miles_awarded': miles_to_award,
                    'message': f'感谢您的评价！您获得了{miles_to_award}里数。'
                }, status=status.HTTP_201_CREATED)
            else:
                # 已经获得里数的情况
                return Response({
                    'survey': serializer.data,
                    'miles_awarded': 0,
                    'message': '评价提交成功，但您已对该菜品获得过里数奖励。'
                }, status=status.HTTP_201_CREATED)
        else:
            # 没有菜品关联的情况
            return Response({
                'survey': serializer.data,
                'miles_awarded': 0,
                'message': '评价提交成功。'
            }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """删除用餐回馈"""
        from django.http import Http404
        
        survey_id = kwargs.get('pk')
        
        try:
            survey_response = self.get_object()
            actual_id = survey_response.id
            
            # Django 会自动级联删除相关的 PointTransaction（因为 on_delete=CASCADE）
            survey_response.delete()
            
            print(f"✅ 成功删除问卷 ID: {actual_id}")
            
            return Response(
                {'message': f'回馈已删除', 'deleted_id': actual_id},
                status=status.HTTP_200_OK  # 改为 200，方便前端统一处理
            )
        except Http404:
            # 记录已经不存在，可能已被删除
            print(f"⚠️  尝试删除不存在的问卷 ID: {survey_id}")
            return Response(
                {'message': '该回馈已被删除或不存在', 'deleted_id': survey_id},
                status=status.HTTP_200_OK  # 返回 200，因为目标已达成（记录不存在）
            )
        except Exception as e:
            # 记录其他错误信息
            import traceback
            error_detail = traceback.format_exc()
            print(f"❌ 删除回馈失败 (ID: {survey_id}): {str(e)}")
            print(error_detail)
            
            return Response(
                {'error': f'删除失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LeftoverSubmissionViewSet(viewsets.ModelViewSet):
    queryset = LeftoverSubmission.objects.all().order_by('-created_at')  # type: ignore
    serializer_class = LeftoverSubmissionSerializer
    parser_classes = (MultiPartParser, FormParser)

class PeriodicFeedbackViewSet(viewsets.ModelViewSet):
    queryset = PeriodicFeedback.objects.all().order_by('-created_at')  # type: ignore
    serializer_class = PeriodicFeedbackSerializer

    def create(self, request, *args, **kwargs):
        # 创建周期性反馈
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 保存反馈
        periodic_feedback = serializer.save()
        
        # 不再发放里数，直接返回成功响应
        return Response({
            'feedback': serializer.data,
            'message': '感谢您的建议！'
        }, status=status.HTTP_201_CREATED)