from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import *
from .models import *

class UserLoginView(viewsets.ModelViewSet):
	permission_classes = ((AllowAny,))
	queryset = User.objects.all()
	serializer_class = UserLoginSerializer
	http_method_names = ['post']

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context.update({"request": self.request})
		return context

class UserCreationView(viewsets.ModelViewSet):
	permission_classes = ((AllowAny,))
	queryset = User.objects.all()
	serializer_class = UserCreationSerializer
	http_method_names = ['post']

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context.update({"request": self.request})
		return context

class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()
	http_method_names = ['get', 'post','patch']