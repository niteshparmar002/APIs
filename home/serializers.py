from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

class UserSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField('get_token')

	class Meta:
		model = User
		exclude = ('user_permissions','groups','password','is_staff','is_superuser',)
	
	def get_token(self, obj):
		token, created = Token.objects.get_or_create(user=obj)
		return token.key

class UserLoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'password')
		extra_kwargs = {
			'username': {'required': True, 'validators': []},
			'password': {'required': True, 'style': {'input_type': 'password'}},
		}
	
	def to_representation(self, instance):
		request = self.context['request']
		serializer = UserSerializer(instance=instance, context = {'request':request})
		return serializer.data

	def create(self, validated_data):
		is_user = User.objects.filter(username=validated_data['username']).first()
		if is_user is None:
			raise serializers.ValidationError({"detail":"Sorry, we couldn't find an account with this username."})
		if not is_user.check_password(validated_data['password']):
			raise serializers.ValidationError({"detail":"Sorry, your password was incorrect. Please double-check your password."})
		if is_user and not is_user.is_active:
			raise serializers.ValidationError({"notActive":'Account is not activated.'})
		user = authenticate(username=validated_data['username'], password=validated_data['password'],)
		if user is not None:
			return user
		raise serializers.ValidationError({"detail":"Sorry, your password was incorrect. Please double-check your password."})

class UserCreationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type': 'password'},write_only=True)
	cpassword = serializers.CharField(style={'input_type': 'password'},write_only=True)

	class Meta:
		model = User
		fields = ('username','password','cpassword','email','first_name','last_name',)
		extra_kwargs = {
			'first_name': {'required': True},
			'last_name': {'required': True},
		}

	def validate(self, data):
		if data['password'] != data['cpassword']:
			raise serializers.ValidationError({"cpassword":['Passwords do not match']})
		return data

	def to_representation(self, instance):
		serializer = UserSerializer(instance=instance)
		return serializer.data

	def create(self, validated_data):
		user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'], first_name = validated_data['first_name'], last_name = validated_data['last_name'])
		return user


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'