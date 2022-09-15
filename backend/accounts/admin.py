from django.contrib import admin
from .models import AdminUser

# Register your models here.
@admin.register(AdminUser)
class AdminUserInvester(admin.ModelAdmin):
    list_display = ["name", "email", "last_login", "created_at", "updated_at"]
    list_display_links = ["name"]
