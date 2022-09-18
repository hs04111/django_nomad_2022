from django.contrib import admin
from .models import Room, Amenity

# Register your models here.


@admin.action(description="Set all prices to zero")
def set_prices(model_admin, request, queryset):

    # model_admin: 밑의 클래스에 들어가있는 ModelAdmin
    # request: 어떤 requst가 들어왔는가? 누가 action 요청?
    # queryset: 패널에서 선택된 object들
    for room in queryset:
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (set_prices,)
    list_display = (
        "name",
        "price",
        "kind",
        "owner",
    )

    list_filter = (
        "price",
        "rooms",
        "amenities",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "price",
        "name",
    )


@admin.register(Amenity)
class AnemityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "updated_at",
    )
