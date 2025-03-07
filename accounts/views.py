from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.http import JsonResponse




def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Mã hóa mật khẩu
            user.save()
            login(request, user)
            return redirect('home')  # Điều hướng về trang chủ
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

User = get_user_model()

# Kiểm tra xem người dùng có phải là admin không
def is_admin(user):
    return user.is_superuser

# Quản lý người dùng
def manage_users(request):
    # Kiểm tra xem người dùng có phải là admin không
    if not request.user.is_superuser:
        return redirect('home')  # Nếu không phải admin, chuyển về trang chủ (hoặc trang khác bạn muốn)
    
    # Hiển thị danh sách người dùng (hoặc các thao tác quản lý người dùng khác)
    users = User.objects.all()  # Lấy tất cả người dùng
    return render(request, 'accounts/manage_users.html', {'users': users})

# # Khóa người dùng
# def block_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)
    
#     if request.user.is_superuser:  # Chỉ admin mới có quyền khóa
#         user.is_blocked = True  # Đánh dấu người dùng là bị khóa
#         user.save()
#         return JsonResponse({'status': 'success', 'message': f"Tài khoản {user.username} đã bị khóa."})
#     else:
#         return JsonResponse({'status': 'error', 'message': "Bạn không có quyền khóa tài khoản này."})

# Khóa hoặc mở khóa tài khoản người dùng
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "Bạn không thể khóa tài khoản của chính mình.")
        return redirect('manage_users')
    
    # Đổi trạng thái khóa tài khoản
    user.is_blocked = True
    user.save()
    messages.success(request, f"Tài khoản {user.username} đã bị khóa.")
    return redirect('manage_users')

def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "Bạn không thể mở khóa tài khoản của chính mình.")
        return redirect('manage_users')
    
    # Đổi trạng thái mở khóa tài khoản
    user.is_blocked = False
    user.save()
    messages.success(request, f"Tài khoản {user.username} đã được mở khóa.")
    return redirect('manage_users')
# # Mở khóa người dùng
# def unblock_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)

#     if request.user.is_superuser:  # Chỉ admin mới có quyền mở khóa
#         user.is_blocked = False  # Đánh dấu người dùng là hoạt động
#         user.save()
#         return JsonResponse({'status': 'success', 'message': f"Tài khoản {user.username} đã được mở khóa."})
#     else:
#         return JsonResponse({'status': 'error', 'message': "Bạn không có quyền mở khóa tài khoản này."})

# # Khóa hoặc mở khóa tài khoản người dùng
# @user_passes_test(is_admin)
# def toggle_block_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)

#     # Không cho phép admin khóa chính tài khoản của mình
#     if user == request.user:
#         messages.error(request, "Bạn không thể khóa tài khoản của chính mình.")
#         return redirect('manage_users')

#     # Khóa hoặc mở khóa tài khoản người dùng
#     user.is_blocked = not user.is_blocked
#     user.save()
#     status = "bị khóa" if user.is_blocked else "được mở khóa"
#     messages.success(request, f"Tài khoản {user.username} đã {status}.")
#     return redirect('manage_users')

@user_passes_test(is_admin)
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Nếu người dùng bị khóa, thông báo và không cho phép reset mật khẩu
    if user.is_blocked:
        messages.error(request, "Tài khoản của bạn đã bị khóa, không thể reset mật khẩu.")
        return redirect('manage_users')

    # Nếu là request POST (khi reset mật khẩu)
    if request.method == "POST":
        # Tạo mật khẩu mặc định
        default_password = "newpassword123"
        
        # Đặt mật khẩu mới cho user
        user.set_password(default_password)  # Đặt mật khẩu mới
        user.save()  # Lưu lại thay đổi
        update_session_auth_hash(request, user)  # Cập nhật session sau khi đổi mật khẩu

        messages.success(request, f"Mật khẩu của {user.username} đã được reset thành {default_password}.")
        return redirect('manage_users')
    else:
        # Nếu không phải POST, chỉ hiển thị form
        form = PasswordChangeForm(user)

    return render(request, 'accounts/reset_password.html', {'form': form, 'user': user})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Lấy user từ form
            user = form.get_user()

            # Đăng nhập người dùng
            login(request, user)

            # Kiểm tra nếu là admin
            if user.is_superuser:
                # Nếu là admin, chuyển đến trang quản lý người dùng
                return redirect('manage_users')  # 'manage_users' là tên của URL quản lý người dùng
            else:
                # Nếu là người dùng bình thường, chuyển đến trang post_list
                return redirect('post_list')  # 'post_list' là tên của URL trang danh sách bài viết

        else:
            messages.error(request, "Invalid login credentials")

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Đường dẫn đến mẫu trang login của bạn

    def form_valid(self, form):
        user = form.get_user()

        if user.is_blocked:
            messages.error(self.request, "Tài khoản của bạn đã bị khóa.")
            return redirect('login')  # Quay lại trang login nếu bị khóa

        return super().form_valid(form)