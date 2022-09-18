from django.db import models

# Create your models here.


class CommonModel(models.Model):
    """Common Model Definition"""

    # CommonModel은 class Meta로 abstract를 가지기 때문에
    # 데이터베이스에 Common의 table이 만들어지지 않을 것이다.

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True
