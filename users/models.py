from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 장고의 유저 모델을 상속받아 확장, 커스텀으로 사용하려면 아래처럼 사용한다.
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/


class User(AbstractUser):

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False, verbose_name="Are you host?")
