from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import apis

# api modelviewset setting 
app_name = "auth"
router = DefaultRouter()
router.register(app_name, apis.AdminRegisterAPI) # 2개 url 를 만들어줌 

urlpatterns = [
    path("api-v1/", include(router.urls))
]
