from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# UserAdmin은 그냥 ModelAdmin보다 기능이 많다.
# 기본으로 장고에서 주어진 유저 모델을 사용하면 적용되는 관리자 패널을 상속하여 쓰는것


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # 우리가 User에서 커스텀으로 name과 is_host를 정해주고
    # first_name 등을 editable=False로 두었기 때문에, 빼야 하므로
    # fieldsets는 반드시 오버라이딩해야 한다.

    fieldsets = (
        ("Profile", {"fields": ("username", "password", "is_host", "name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined"), "classes": ("collapse",)},
        ),
    )

    list_display = ("username", "email", "name", "is_host")
