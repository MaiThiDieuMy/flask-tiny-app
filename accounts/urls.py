from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin
from .views import CustomLoginView

from .views import login_view

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Đảm bảo chỉ có một đường dẫn duy nhất cho 'block_user' và 'unblock_user'
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),

    path('manage_users/', views.manage_users, name='manage_users'),  # Trang quản lý user cho admin
    
    # Đường dẫn reset password
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
    
