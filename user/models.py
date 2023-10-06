from django.db import models
from django.contrib.auth.models import User

# email과 password(소셜로그인의 경우에는 유저의 이름으로 대체), profile_image(디폴트는 기본 이미지)만 사용
class User(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_image_url = models.CharField(max_length=500, blank=True, default="")
    
    class Meta:
        managed = True
        db_table = 'CustomUser'