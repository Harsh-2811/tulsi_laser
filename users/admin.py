from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from users.models import Technician, APKs
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets  + (
            (None, {'fields': ('role','push_token')}),
    )


admin.site.register(get_user_model(), CustomUserAdmin)

admin.site.register(Technician)
admin.site.register(APKs)