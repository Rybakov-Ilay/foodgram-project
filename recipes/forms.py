from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "description", "image", "cooking_time", "tags")
        widgets = {"tags": forms.CheckboxSelectMultiple(), }

        help_texts = {
            "title": _("Заполните заголовок рецепта."),
            "description": _("Заполните описание рецепта"),
            "image": _("Выберите изображение для рецепта"),
            "cooking_time": _("Заполните время приготовления блюда"),
        }
