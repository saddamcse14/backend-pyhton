from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'age']

    def create(self, validated_data):
        age = validated_data.pop('age', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        if age is not None:
            Profile.objects.create(user=user, age=age)
        return user


class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source='profile.age', default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'age', 'date_joined']