from django.contrib.auth import get_user_model
from django.db import models
from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel

User = get_user_model()


class Tag(TimeStampedModel):
    name = models.CharField(verbose_name="тег", max_length=50)
    slug = models.SlugField(max_length=20)
    color = models.CharField(verbose_name="цвет чекбокса", max_length=20)

    class Meta:
        ordering = ["id"]
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Ingredient(TimeStampedModel):
    name = models.CharField(
        verbose_name="название",
        max_length=250,
        db_index=True
    )
    measure_unit = models.CharField(
        verbose_name="единица измерения",
        max_length=50
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"

    def __str__(self):
        return f"{self.name}, {self.measure_unit}"


class Recipe(TimeStampedModel):
    title = models.CharField(
        verbose_name="название",
        max_length=250,
        db_index=True)

    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        verbose_name="картинка",
        upload_to="upload"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="время приготовления в минутах",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="автор",
        related_name="recipes",
        db_index=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient"
    )
    tags = models.ManyToManyField(Tag, related_name="recipes")

    class Meta:
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"
        ordering = ["-created"]

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="рецепт",
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="ингредиент",
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="количество",
        null=False,
        default=10,
    )
    created = AutoCreatedField(verbose_name="дата создания")

    class Meta:
        verbose_name = "ингредиент рецепта"
        verbose_name_plural = "ингредиенты рецепта"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="recipe_ingredients"
            )
        ]


class Favorite(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="автор",
        related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
        related_name="favorites",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "recipe"],
                name="unique_favorites"
            )
        ]
        verbose_name = "избранное"
        verbose_name_plural = "избранные"

    def __str__(self):
        return f"{self.author}-{self.recipe}"


class Subscribe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="автор"
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="подписчик",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "follower"],
                name="unique_subscribes"
            )
        ]
        verbose_name = "подписка"
        verbose_name_plural = "подписки"

    def __str__(self):
        return f"{self.follower} подписался на {self.author}"


class Purchase(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="автор",
        related_name="purchases"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
        related_name="purchases",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "recipe"],
                name="unique_purchases"
            )
        ]
        verbose_name = "список покупок"
        verbose_name_plural = "списки покупок"

    def __str__(self):
        return f"{self.author}-{self.recipe}"
