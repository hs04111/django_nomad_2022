from django.contrib import admin
from .models import Review


class RatingFilter(admin.SimpleListFilter):
    parameter_name = "input_rating"
    title = "Filter by rating"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, queryset):
        rating = request.GET.get("input_rating")
        if rating == "good":
            return queryset.filter(rating__gte=3)
        elif rating == "bad":
            return queryset.filter(rating__lt=3)
        else:
            return queryset


class WordFilter(admin.SimpleListFilter):
    parameter_name = "word"
    title = "Filter by Word"

    def lookups(self, request, model_admin):

        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, queryset):
        # 밑의 word는 다음과 같이 구할 수도 있다: request.GET['word']
        word = self.value()
        if word:
            return queryset.filter(payload__contains=word)
        else:
            return queryset


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ("__str__", "payload")
    list_filter = (
        RatingFilter,
        "rating",
        "user__is_host",
        "room__category",
        WordFilter,
    )
