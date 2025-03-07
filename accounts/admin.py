from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_blocked', 'is_staff')
    list_filter = ('is_active', 'is_blocked', 'is_staff')
    actions = ['block_users', 'unblock_users', 'reset_password']

    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)
    block_users.short_description = "Block selected users"

    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)
    unblock_users.short_description = "Unblock selected users"

    def reset_password(self, request, queryset):
        for user in queryset:
            user.set_password("newpassword123")  # Reset về mật khẩu mặc định
            user.save()
    reset_password.short_description = "Reset password for selected users"

admin.site.register(CustomUser, CustomUserAdmin)
