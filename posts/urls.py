from django.urls import path
from . import views
from .views import logout_view, login_view

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),  # Trang danh sách bài viết
    path('create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Thêm URL xóa bài viết
    # Thêm URL cho Manage Blog
    path('manage/', views.manage_blog, name='manage_blog'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
]
