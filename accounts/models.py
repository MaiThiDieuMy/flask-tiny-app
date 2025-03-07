from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')])

    def __str__(self):
        return self.user.username

class CustomUser(AbstractUser):
    is_blocked = models.BooleanField(default=False)

    # Thêm related_name để tránh xung đột với các trường mặc định của User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Đổi tên liên kết để tránh xung đột
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of these groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Đổi tên liên kết để tránh xung đột
        blank=True,
        help_text='Specific permissions for this user.'
    )   
