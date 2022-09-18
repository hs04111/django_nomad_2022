from django.db import models
from common.models import CommonModel

# Create your models here.


class Experience(CommonModel):

    """Experience model definition"""

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, default="")
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="experiences",
    )


class Perk(CommonModel):

    """What is included on an Experience"""

    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=150,
    )
    details = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    explanation = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
