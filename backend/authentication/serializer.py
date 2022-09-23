from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import AdminUser, NormalUser
from argon2 import PasswordHasher


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
    
    def validate_password2(self, data):
        if self.initial_data["password"] == data:
            return data
        raise ValidationError(detail="비밀번호가 같지 않습니다", code="password_mismatch")
    
    def create(self, validated_data):
        del validated_data["password2"]
        
        password = validated_data.get("password")
        user_save = AdminUser.objects.create(**validated_data)
        user_save.set_password(password)
        user_save.save()
        
        return user_save
        
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