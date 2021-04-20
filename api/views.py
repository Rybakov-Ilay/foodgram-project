from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Purchase, Recipe, Subscribe

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscribeSerializer)

User = get_user_model()


class CreateResponseMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class IngredientAPIView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "^name",
    ]


class SubscribeViewSet(CreateResponseMixin, viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=kwargs["pk"])
        subscribe = author.following.filter(follower=request.user)
        return Response({"success": True if subscribe.delete() else False})


class FavoriteViewSet(CreateResponseMixin, viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs["pk"])
        favorite = recipe.favorites.filter(author=request.user)
        return Response({"success": True if favorite.delete() else False})


class PurchaseViewSet(CreateResponseMixin, viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs["pk"])
        purchase = recipe.purchases.filter(author=request.user)
        return Response({"success": True if purchase.delete() else False})
