from .models import User
from rest_framework import serializers
from .exceptions import FieldValidationError, UserNotFoundException
from django.db.models import Q

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

# User Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    def validate(self, data):
        self._username = data.get("username", "")
        self._password = data.get("password", "")
        if self._username == "":
            raise FieldValidationError("Email is required")

        if self._password == "":
            raise FieldValidationError("Password is required")

        users = User.objects.filter(
            Q(username=self._username) | Q(email=self._username)
        )
        if users.count() != 1:
            raise UserNotFoundException()

        user = users[0]

        if not user.authenticate(self._password):
            raise UserNotFoundException()

        return user


class SessionSerializer(serializers.Serializer):
    username = serializers.CharField()
