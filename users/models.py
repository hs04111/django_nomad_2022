from locale import currency
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 장고의 유저 모델을 상속받아 확장, 커스텀으로 사용하려면 아래처럼 사용한다.
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        # Tuple 첫번째: 데이터베이스로 갈 문자열, 두번째: 실제로 사용할 레이블
        # 첫번째는 max_length보다 작아야 한다
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        En = ("en", "English")

    class CurrencyChoices(models.TextChoices):

        # 튜플은 괄호를 하지 않아도 작동한다.
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
        verbose_name="Are you host?",
    )

    # ImageField는 Pillow를 필요로 한다. poetry add Pillow 실행
    # blank는 null과 다르다. blank는 fom에서 required의 여부를 결정하고
    # null은 데이터베이스에 null이 들어가는지의 여부이다.
    avatar = models.ImageField(
        blank=True,
    )

    # choices를 사용하면, admin에서 옵션을 선택할 수 있도록 변경이 가능하다.
    # 사용하려면 위처럼 class를 작성하여 아래와 같이 사용한다.
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=10,
        choices=CurrencyChoices.choices,
    )
