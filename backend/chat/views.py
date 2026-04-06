from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ChatSession, ChatMessage, FAQEntry
from menu.models import Dish

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_with_chef(request):
    dish_id = request.data.get('dish_id')
    if not dish_id:
        return Response({'error': 'dish_id is required'}, status=400)

    dish = Dish.objects.filter(id=dish_id).first()
    if not dish:
        return Response({'error': 'dish not found'}, status=404)

    lang = request.data.get('lang', 'zh')
    question = (request.data.get('question') or '').strip()
    if not question:
        return Response({'error': 'question is required'}, status=400)

    faqs = FAQEntry.objects.filter(dish_id=dish_id, lang=lang)
    hit = None
    for f in faqs:
        if f.question.strip().lower() in question.lower():
            hit = f
            break

    session_id = request.data.get('session_id')
    try:
        if not session_id:
            s = ChatSession.objects.create(
                user=request.user if request.user.is_authenticated else None,
                dish=dish
            )
            session_id = s.id
        else:
            s = ChatSession.objects.get(id=session_id)

        ChatMessage.objects.create(session=s, role='user', content=question)

        if hit:
            ans = hit.answer
        else:
            ans = '（AI 虚拟厨师占位回复）后续可接入 RAG/LLM：提供食材文化、历史典故、烹饪技巧等。'

        ChatMessage.objects.create(session=s, role='assistant', content=ans)
        return Response({'session_id': session_id, 'answer': ans})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
