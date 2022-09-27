from django.db import models
from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    def __str__(self) -> str:
        return "Photo File"

    file = models.URLField()
    description = models.CharField(max_length=140)
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="medias",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="medias",
    )


class Video(CommonModel):
    def __str__(self) -> str:
        return "Video File"

    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )
