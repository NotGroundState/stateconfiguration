from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import apis

# api modelviewset setting 
app_name = "auth"
router = DefaultRouter()

router.register("auth-register", apis.AdminRegisterAPI)
router.register("normal-register", apis.UserRegisterAPI)
router.register("auth", apis.AdminInformAPI)
router.register("user", apis.UserInformAPI)

urlpatterns = [
    path("api-v1/", include(router.urls)),
    path("api-v1/auth-login", apis.AdminLoginAPI.as_view()),
    path("api-v1/user-login", apis.UserLoginAPI.as_view()),
]
