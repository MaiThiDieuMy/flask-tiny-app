from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

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
