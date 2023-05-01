from rest_framework import routers
from django.urls import path

from .views import signup_function, token_function

router_v1 = routers.DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/', signup_function, name='signup'),
    path('v1/auth/token/', token_function, name='token'),
]
