from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=6)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

        def create(self, validate_data):
            user = User.objects.create_user(
                
                email=validate_data["email"],
                password=validate_data["password"],
            )
            return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]