from django.db import models
from common.models import CommonModel


class Category(CommonModel):

    """Room or Experience categories model definition"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(
        max_length=11,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self):
        return f"{self.kind}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"


# Create your models here.
