from decimal import Decimal

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient, Recipe, Tag


def paginator_mixin(request, queryset):
    paginator = Paginator(queryset, settings.PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page, paginator


def get_ingredients(request):
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith("nameIngredient"):
            num = key.partition("_")[-1]
            ingredients[name] = post[f"valueIngredient_{num}"]
    return ingredients


def save_recipe(request, form):
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()

    objs = []
    ingredients = get_ingredients(request)

    for name, quantity in ingredients.items():
        ingredient = get_object_or_404(Ingredient, name=name)
        objs.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=Decimal(quantity.replace(",", ".")),
            )
        )

    RecipeIngredient.objects.bulk_create(objs)
    form.save_m2m()
    return recipe


def edit_recipe(request, form, instance):
    RecipeIngredient.objects.filter(recipe=instance).delete()
    return save_recipe(request, form)


def filter_recipes_by_tag(request):
    tags = request.GET.getlist("tags")
    if tags:
        recipes = (
            Recipe.objects.prefetch_related("author", "tags")
            .filter(tags__slug__in=tags)
            .distinct()
        )
    else:
        recipes = Recipe.objects.all()
    all_tags = Tag.objects.all()
    return recipes, all_tags
