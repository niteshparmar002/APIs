from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register('login', api.UserLoginView, basename='api_login')
router.register('signup', api.UserCreationView, basename='api_sign')
router.register('post', api.PostViewSet, basename='post')

urlpatterns = [
	path('', include(router.urls)),
]