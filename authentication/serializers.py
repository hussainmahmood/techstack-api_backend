from .models import User
from rest_framework import serializers
from .exceptions import FieldValidationError, UserNotFoundException, UserAlreadyPresentException
from django.db.models import Q

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

# User Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class RegisterSerializer(serializers.Serializer):
    confirm_password = serializers.CharField()
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
    
    def validate(self, data):
        self.name = data.get("name", "")
        self.email = data.get("email", "")
        self.password = data.get("password", "")
        self.confirm_password = data.get("confirm_password", "")
        if self.name == "":
            raise FieldValidationError("Name is required")

        if self.email == "":
            raise FieldValidationError("Email is required")

        if self.password == "":
            raise FieldValidationError("Password is required")
        
        if self.confirm_password != self.password:
             raise FieldValidationError("Passwords do not match")
        
        users = User.objects.filter(email=self.email)
        if users.count() != 0:
            raise UserAlreadyPresentException()
        
        user = User(name=self.name, email=self.email)
        user.encrypt(self.password)
        user.save()

        return user




class LoginSerializer(serializers.Serializer):    
    def validate(self, data):
        self._email = data.get("email", "")
        self._password = data.get("password", "")
        if self._email == "":
            raise FieldValidationError("Email is required")

        if self._password == "":
            raise FieldValidationError("Password is required")

        users = User.objects.filter(email=self._email)
        if users.count() != 1:
            raise UserNotFoundException()

        user = users.first()

        if not user.authenticate(self._password):
            raise UserNotFoundException()

        return user
