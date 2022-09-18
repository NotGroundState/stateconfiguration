from rest_framework import serializers
from accounts.models import AdminUser, NormalUser


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["email", "name", "password"]
    
    def validate(self, attrs):
        # OrderedDict([('email', 'robots@test.com'), ('name', '황도현'), ('password', '123123123!!')])
        print(super().validate(attrs))
        return super().validate(attrs)