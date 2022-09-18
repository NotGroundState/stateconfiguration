from rest_framework import serializers
from accounts.models import AdminUser, NormalUser


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["email", "name", "password", "created_at", "updated_at"]
        extra_kargs = {
            "password": {
                "write_only": True
            }
        }
        
    def create(self, validated_data):
        pass 

    def validate(self, attrs):
         pass