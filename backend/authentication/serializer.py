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
        fields = ["email", "name", "password", "password2"]
        extra_kwargs = {
            'password' : {
                'write_only': True,
                "style": {"input_type": "password"}
            }
        }
        
    def validate_email(self, value: str) -> str:
        try:
            AdminUser.objects.get(email=value)
        except AdminUser.DoesNotExist:
            return value
        else:
            raise ValidationError(detail="존재하는 이메일 입니다")
    
    def validate_password(self, value: str) -> str:
        if len(value) > 8:
            return value
        raise ValidationError(detail="비밀번호는 8자 이상 입력해주세요!")

    def validate(self, data: str) -> Dict:
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")
        
        if self.validate_email(email):
            if self.validate_password(password):
                if password == password2:
                    return {
                        "email": email,
                        "name": data.get("name"),                        
                    }
            elif password != password2:
                raise ValidationError(detail="비밀번호가 맞는지 확인해주세요")
          

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = NormalUser
        fields = ["email", "password", "password2"]
        extra_kwargs = {
            'password' : {
                'write_only': True,
                "style": {"input_type": "password"}
            }
        }