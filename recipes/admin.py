from django.contrib import admin

from .models import Favorite, Ingredient, Purchase, Recipe, Subscribe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measure_unit")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "description",
    )
    list_filter = ("title",)
    list_per_page = 20
    search_fields = (
        "title",
        "author",
    )


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
