from argon2 import PasswordHasher
from typing import Any, List

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

"""
table architecutre 수정 해야함 
"""

class UserManager(BaseUserManager):
    use_in_migrations: bool = True
    
    def _create_superuser(self, email: str, name: str, password: PasswordHasher, **extra_field):
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
    
    def create_superuser(self, email: str, name: str, password: PasswordHasher, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저 권한은 관리자에게 문의하세요")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저 권한은 관리자에게 문의하세요")
        
        return self._create_superuser(email=email, name=name, password=password, **extra_fields)
    
    

class BasicInform(models.Model):
    email = models.EmailField(
        verbose_name=_("email"), max_length=50, 
        blank=False, null=False, unique=True,
    )
    password = models.CharField(
        verbose_name=_("password"), max_length=128,
        blank=False, null=False, validators=[MinLengthValidator(8, message="8자 이상 입력해주세요..!")]
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: bool = True
        
    
class AdminUser(AbstractBaseUser, PermissionsMixin, BasicInform):
    name = models.CharField(
        verbose_name=_("name"), max_length=6, 
        blank=False, null=False
    )

    # 필수 setting 
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    EMAIL_FIELD: str = "email"
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["name", "password"]
    objects: BaseUserManager[Any] = UserManager()
        
    def __str__(self) -> str:
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", args=[self.pk])
    
    def has_perms(self, perm_list, obj) -> bool:
        return True
    
    def has_module_perms(self, app_label: str) -> bool:
        return True
    
    class Meta:
        db_table: str = "admin_user"
        verbose_name = _("admin_user")
        verbose_name_plural = _("admin_users")

        
class NormalUser(BasicInform):   
    class Meta:
        db_table: str = "normal_user"
        verbose_name = _("normal_user")
        verbose_name_plural = _("normal_users")
            
    def __str__(self):
        return self.email

    # def get_absolute_url(self):
    #     return reverse("", args=[self.pk])


class NormalUserPermission(models.Model):
    normal_user = models.OneToOneField(
        NormalUser, on_delete=models.CASCADE, primary_key=True
    )
    adv = models.BooleanField(verbose_name=_("adv_accept"))
    permission = models.BooleanField(verbose_name=_("permission_accept"))
    check_email = models.BooleanField(verbose_name=_("cheking_email"))
    
    class meta:
        db_table: str = "user_permission"
        verbose_name = _("user_permission")
        verbose_name_plural = _("user_permission")

    def __str__(self) -> str:
        return f"{self.normal_user}"
