from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "role"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            phone=validated_data.get("phone"),
            role=validated_data.get("role", "customer"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # email OR phone OR username
    password = serializers.CharField()

    def validate(self, data):
        identifier = data.get("identifier")
        password = data.get("password")

        user = User.objects.filter(email=identifier).first()

        if not user:
            user = User.objects.filter(phone=identifier).first()

        if not user:
            user = User.objects.filter(username=identifier).first()

        if user and user.check_password(password):
            data["user"] = user
            return data

        raise serializers.ValidationError("Invalid credentials")
