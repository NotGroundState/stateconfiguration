from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

from argon2 import PasswordHasher
from typing import Any, List


# 시간 획일화 
class AdminLoginTimeStemp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: bool = True


class UserManager(BaseUserManager):
    use_in_migrations: bool = True
    
    def _create_user(self, email: str, name: str, password: PasswordHasher, **extra_field):
        if not email:
            raise ValueError("이미 이메일이 존재합니다")
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            password=PasswordHasher().hash(password=password),
            **extra_field
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email: str, name: str, password: PasswordHasher, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)
        
        return self._create_user(email=email, name=name, password=password, **extra_fields)
    
    def create_superuser(self, email: str, name: str, password: PasswordHasher, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저 권한은 관리자에게 문의하세요")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저 권한은 관리자에게 문의하세요")
        
        return self._create_user(email=email, name=name, password=password, **extra_fields)
    
    
class AdminUser(AbstractBaseUser, PermissionsMixin, AdminLoginTimeStemp):
    email = models.EmailField(
        verbose_name=_("email"), max_length=50, 
        blank=False, null=False, unique=True
    )
    name = models.CharField(
        verbose_name=_("name"), max_length=6, 
        blank=False, null=False
    )

    # 필수 setting 
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    EMAIL_FIELD: str = "email"
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["name", "password"]
    objects: BaseUserManager[Any] = UserManager()
    
    def has_perms(self, perm_list, obj) -> bool:
        return True
    
    def has_module_perms(self, app_label: str) -> bool:
        return True