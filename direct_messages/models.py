from django.db import models
from common.models import CommonModel

# Create your models here.


class ChattingRoom(CommonModel):

    """Chat Room Definition"""

    def __str__(self) -> str:
        return "Chatting Room"

    users = models.ManyToManyField(
        "users.User",
    )


class Message(CommonModel):

    """Message Model Definition"""

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_messages",
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="direct_messages",
    )
