from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# User model
class User(AbstractBaseUser):
    username = None
    email = models.EmailField( unique=True, blank=False )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
