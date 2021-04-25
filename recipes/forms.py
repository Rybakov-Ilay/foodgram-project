from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "description", "image", "cooking_time", "tags")
        widgets = {"tags": forms.CheckboxSelectMultiple(), }

        help_texts = {
            "title": "Заполните заголовок рецепта.",
            "description": "Заполните описание рецепта",
            "image": "Выберите изображение для рецепта",
            "cooking_time": "Заполните время приготовления блюда",
        }
