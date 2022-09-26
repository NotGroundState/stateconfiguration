from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import AdminUser, NormalUser


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
        

# 분권화 
class AdminSerializer(RegisterSerializer):  
    class Meta(RegisterSerializer.Meta):
        model = AdminUser  
    
        
class UserSerializer(RegisterSerializer):    
    class Meta(RegisterSerializer.Meta):
        model = NormalUser
