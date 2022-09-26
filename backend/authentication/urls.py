from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import apis

# api modelviewset setting 
app_name = "auth"
router = DefaultRouter()

router.register("auth", apis.AdminRegisterAPI)
router.register("normal", apis.UserRegisterAPI)

router.register("auser", apis.AdminInformAPI)
router.register("user", apis.UserInformAPI)

urlpatterns = [
    path("api-v1/", include(router.urls)),
]
