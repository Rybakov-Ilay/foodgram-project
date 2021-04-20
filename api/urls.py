from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteViewSet, IngredientAPIView, PurchaseViewSet,
                       SubscribeViewSet)

v1_router = DefaultRouter()

v1_router.register("favorites", FavoriteViewSet)
v1_router.register("purchases", PurchaseViewSet)
v1_router.register("subscriptions", SubscribeViewSet)

v1_urlpatterns = [path("ingredients/", IngredientAPIView.as_view())]

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/", include(v1_urlpatterns)),
]
