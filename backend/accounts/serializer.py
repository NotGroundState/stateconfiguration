from typing import Dict, List
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import AdminUser, NormalUser


# 회원 가입 일원화 
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        fields = ["email", "password", "password2", "created_at", "updated_at"]
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
        
    def create(self, validated_data: dict) -> None:
        del validated_data["password2"]
        
        password = validated_data["password"]
        user_save = super().create(validated_data)
        user_save.set_password(password)
        user_save.save()
        
        return user_save
    

class LoginSerializer(serializers.ModelSerializer):
    error_messages = {
        "login": "아이디와 비밀번호를 입력해주세요",
    }
    
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        fields: List[str] = ["email", "password"]


    def validate(self, data):
        email: str = data.get("email")
        password: PasswordHasher = data.get("password")
        
        try:
            user =  self.Meta.model.objects.get(email=email)
            user_password: PasswordHasher = user.password 
            pc: bool = PasswordHasher().verify(str(user_password).strip("argon2"), password)
            if pc is True:
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)
                data = {
                    "msg": "로그인 성공",
                    "info": {
                        "email": user.email,
                        "refresh": refresh,
                        'access': access
                    }
                }
                return data
        except (self.Meta.model.DoesNotExist, VerifyMismatchError):
            raise ValidationError(self.error_messages)


# 분권화 
class AdminSerializer(RegisterSerializer):  
    class Meta(RegisterSerializer.Meta):
        model = AdminUser  
    
        
class UserSerializer(RegisterSerializer):    
    class Meta(RegisterSerializer.Meta):
        model = NormalUser


# 로그인
class AdminLoginSerializer(LoginSerializer):  
    class Meta(LoginSerializer.Meta):
        model = AdminUser  
    
        
class UserLoginSerializer(LoginSerializer):    
    class Meta(LoginSerializer.Meta):
        model = NormalUser