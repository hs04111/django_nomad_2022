from django.db import models
from common.models import CommonModel

# Create your models here.


class Room(CommonModel):

    # 기본 field들에 대한 설명은 User 모델 참조
    # CommonModel은 class Meta로 abstract를 가지기 때문에
    # 데이터베이스에 Common의 table이 만들어지지 않을 것이다.

    """Room Model Definition"""

    def __str__(self):
        return self.name

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return "No reviews"
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

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
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )
    amenities = models.ManyToManyField("rooms.Amenity")
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="rooms",
    )


class Amenity(CommonModel):

    """Amenity Definition"""

    def __str__(self) -> str:
        return self.name

    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Amenities"
