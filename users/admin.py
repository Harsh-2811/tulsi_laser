from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets  + (
            (None, {'fields': ('role',)}),
    )


admin.site.register(get_user_model(), CustomUserAdmin)