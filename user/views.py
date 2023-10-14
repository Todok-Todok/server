# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 소셜로그인
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

import requests
from django.shortcuts import redirect
from .models import User
from allauth.socialaccount.models import SocialAccount
import secret

from rest_framework.decorators import api_view

'''
1. google_login 실행 후 로그인 성공 시, Callback 함수로 Code 값 전달받음
2. 받은 Code로 Google에 Access Token 요청
3.  Access Token으로 Email 값을 Google에게 요청
4. 전달받은 Email, Access Token, Code를 바탕으로 회원가입/로그인 진행
'''
state = getattr(secret, 'STATE')
BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'user/google/callback/'

# Create your views here.
# 프론트가 구현할 함수
def google_login(request):
    """
    Code Request
    """
    client_id = getattr(secret, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    # scope : email과 profile 요청 !
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope=email profile")

@api_view(('POST','GET'))
def google_callback(request):
    print("콜백 들어옴")
    client_id = getattr(secret, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(secret, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')

    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    access_token = token_req_json.get('access_token')
    """
    UserInfo Request
    """
    info_req = requests.get(
        f"https://www.googleapis.com/userinfo/v2/me?access_token={access_token}")
    email_req_status = info_req.status_code
    if email_req_status != 200:
        return Response({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    info_req_json = info_req.json()
    email = info_req_json.get('email')
    print(info_req_json)

    """
    Signup or Signin Request
    """
    try:
        print("try문 들어옴")
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return Response({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return Response({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}user/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return Response(accept_json) # 로그인 폼에 맞게 json 형식 수정 필요
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        print("access token = "+access_token)
        accept = requests.post(
            f"{BASE_URL}user/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return Response(accept_json)
    
class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client