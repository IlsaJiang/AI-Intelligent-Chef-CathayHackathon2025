from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([AllowAny])
def choose_meal_bridge(request):
    payload = request.data
    # TODO: integrate with external Cathay API here.
    return Response({'status':'stub-ok', 'forwarded': payload})
