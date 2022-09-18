from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .serializer import AdminUserSerializer
from accounts.models import AdminUser, NormalUser


class AdminRegisterAPI(ModelViewSet):
    queryset = AdminUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = AdminUserSerializer
    
    