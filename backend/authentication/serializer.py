from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import MinLengthValidator 

from accounts.models import AdminUser, NormalUser, TimeStemp
from argon2 import PasswordHasher
from typing import Dict, List


class AdminRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = AdminUser
        fields = ["email", "name", "password", "password2", "created_at", "updated_at"]
        extra_kwargs: Dict[str] = {
            'password' : {
                'write_only': True,
                "style": {"input_type": "password"}
            }
        }

    def validate_email(self, obj) -> str:
        pass
    
    def validate_password(self, obj) -> str:
        pass
    
    def validate(self, attrs) -> Dict:
        pass
    

