from django.db import models
from common.models import CommonModel

# Create your models here.


class Wishlist(CommonModel):

    """Wishlist Model Definition"""

    def __str__(self) -> str:
        return self.name

    name = models.CharField(max_length=150)
    rooms = models.ManyToManyField("rooms.Room")
    experinces = models.ManyToManyField("experiences.Experience")
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="wishlists"
    )
