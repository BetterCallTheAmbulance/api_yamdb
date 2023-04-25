from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
