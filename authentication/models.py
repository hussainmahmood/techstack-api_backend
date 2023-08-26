from django.db import models
from django.contrib.auth.hashers import check_password, make_password

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=70, unique=True, db_index=True)
    password = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def encrypt(self, password):
        self.password = make_password(password)

    def authenticate(self, password):
        if check_password(password, self.password):
            return True
        return False