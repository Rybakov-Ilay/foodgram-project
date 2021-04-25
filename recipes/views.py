from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Purchase, Recipe
from .utils import (edit_recipe, paginator_mixin,
                    save_recipe, filter_recipes_by_tag)

User = get_user_model()


def index(request):
    recipes, all_tags = filter_recipes_by_tag(request)
    page, paginator = paginator_mixin(request, recipes)
    return render(
        request,
        "recipes/indexAuth.html",
        {"page": page, "paginator": paginator, "all_tags": all_tags},
    )


def recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, "recipes/singlePage.html", {"recipe": recipe})


@login_required
def recipe_add(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = save_recipe(request, form)  # noqa
        return redirect("index")
    return render(request, "recipes/formRecipe.html", {"form": form})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)

    if request.user != recipe.author:
        return redirect("recipe_view", recipe_id=pk)

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )

    if form.is_valid():
        edit_recipe(request, form, instance=recipe)
        return redirect("recipe_view", pk=pk)

    context = {"form": form, "recipe": recipe}
    return render(request, "recipes/formChangeRecipe.html", context)


@login_required
def recipe_remove(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.author:
        recipe.delete()
        return redirect("profile", recipe.author)
    return redirect("index")


def profile(request, username):
    recipes, all_tags = filter_recipes_by_tag(request)
    recipes_list = recipes.filter(author__username=username)
    author = get_object_or_404(User, username=username)
    page, paginator = paginator_mixin(request, recipes_list)
    return render(
        request,
        "recipes/authorRecipe.html",
        {
            "page": page,
            "paginator": paginator,
            "all_tags": all_tags,
            "author": author
        }
    )


@login_required
def favorites(request):
    recipes, all_tags = filter_recipes_by_tag(request)
    recipes_list = recipes.filter(favorites__author=request.user)
    page, paginator = paginator_mixin(request, recipes_list)
    return render(
        request,
        "recipes/favorite.html",
        {"page": page, "paginator": paginator, "all_tags": all_tags},
    )


@login_required
def subscriptions(request):
    authors = (
        User.objects.prefetch_related("recipe")
        .filter(following__follower=request.user)
        .annotate(recipe_ingredients=Count("recipe__id"))
    )
    page, paginator = paginator_mixin(request, authors)
    return render(
        request,
        "recipes/myFollow.html",
        {"page": page, "paginator": paginator}
    )


def purchases(request):
    recipes = Recipe.objects.filter(purchases__author=request.user)
    return render(request, "recipes/shopList.html", {"recipes": recipes})


def purchase_remove(request, recipe_id):
    purchase = get_object_or_404(
        Purchase,
        author=request.user,
        recipe__id=recipe_id
    )
    if request.user == purchase.author:
        purchase.delete()
        return redirect("purchases")
    return redirect("index")


@login_required
def get_shoplist(request):
    ingredients = (
        Recipe.objects.prefetch_related("ingredients", "recipe_ingredients")
        .filter(purchases__author=request.user)
        .order_by("ingredients__name")
        .values("ingredients__name", "ingredients__measure_unit")
        .annotate(cnt=Sum("recipe_ingredients__cnt"))
    )

    ingredient_txt = [
        (
            f"\u2022 {item['ingredients__name']} "
            f"({item['ingredients__measure_unit']}) \u2014 {item['cnt']} \n"
        )
        for item in ingredients
    ]
    filename = "shoplist.txt"
    response = HttpResponse(ingredient_txt, content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
