import re
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .serializers import RegisterSerializer, SendOtpSerializer, UserSerializer
from .signals import user_rewarded

User = get_user_model()


class IdentifierTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identifier'] = serializers.CharField(required=False)
        if self.username_field in self.fields:
            self.fields[self.username_field].required = False

    def validate(self, attrs):
        identifier = attrs.get('identifier') or attrs.get(self.username_field)
        if not identifier:
            raise serializers.ValidationError({'identifier': '请输入账号'})

        raw_identifier = identifier.strip()
        candidates = {raw_identifier}
        if '@' in raw_identifier:
            candidates.add(raw_identifier.lower())
        else:
            digits_only = re.sub(r'\D+', '', raw_identifier)
            if digits_only:
                candidates.update({digits_only, f"+{digits_only}"})

        matched_user = None
        for candidate in candidates:
            matched_user = User.objects.filter(username__iexact=candidate).first()
            if matched_user:
                attrs[self.username_field] = matched_user.get_username()
                break

        if not matched_user:
            raise serializers.ValidationError({'identifier': '账号或密码错误'})

        attrs.pop('identifier', None)

        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class IdentifierTokenObtainPairView(TokenObtainPairView):
    serializer_class = IdentifierTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token_serializer = IdentifierTokenObtainPairSerializer(
            data={
                'identifier': serializer.validated_data['identifier'],
                'password': serializer.validated_data['password']
            }
        )
        token_serializer.is_valid(raise_exception=True)

        token_data = token_serializer.validated_data

        reward_data = {
            'miles': 200,
            'points': 10,
            'reason': 'register_login'
        }

        response_data = {
            **token_data,
            'reward': reward_data
        }

        import logging
        logger = logging.getLogger(__name__)
        logger.info(f'注册成功，用户: {user.username}, 奖励数据: {reward_data}, 完整响应: {response_data}')

        user_rewarded.send(
            sender=RegisterView,
            user=user,
            miles=200,
            points=10,
            reason='register_login'
        )

        return Response(response_data, status=status.HTTP_201_CREATED)


class SendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response({'detail': '验证码已发送'}, status=status.HTTP_200_OK)


class MeView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

