from django.contrib import admin
# from django.db.models import Count

from .models import (Favorite, Ingredient, Purchase, Recipe, RecipeIngredient,
                     Subscribe, Tag)


class IngredientnlineAdmin(admin.TabularInline):
    model = RecipeIngredient
    autocomplete_fields = ("ingredient",)
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measure_unit")
    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "description",
    )  # 'get_favorite')
    list_filter = ("tags",)
    inlines = (IngredientnlineAdmin,)
    list_per_page = 20
    search_fields = (
        "title",
        "author",
    )

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset.annotate(added_favorite=Count('favorites'))
    #
    # def get_favorite(self, obj):
    #     return obj.added_favorite

    # get_favorite.short_description = 'добавлен в избранное, раз'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "recipe",
    )
    autocomplete_fields = (
        "author",
        "recipe",
    )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "follower",
    )
    autocomplete_fields = (
        "author",
        "follower",
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "recipe",
    )
    autocomplete_fields = (
        "author",
        "recipe",
    )
