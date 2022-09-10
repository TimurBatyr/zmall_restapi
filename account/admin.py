from django.contrib import admin

from account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'auth_provider']


admin.site.register(User, UserAdmin)
