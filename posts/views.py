from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth import logout,login

def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})
def post_list(request):
    if request.user.is_authenticated:
        posts_list = Post.objects.all().order_by('-id')
        paginator = Paginator(posts_list, 5)  # Hiển thị 5 bài viết mỗi trang
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        return render(request, 'posts/post.html', {'posts': posts})
    else:
        return render(request, 'posts/home.html')  # Người chưa đăng nhập sẽ về home.html

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Tạo nhưng chưa lưu vào database
            post.author = request.user  # Gán tác giả là user đang đăng nhập
            post.save()  # Lưu vào database
            return redirect('post_list')  # Chuyển hướng về danh sách bài viết
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Chỉ cho phép tác giả bài viết hoặc admin xóa
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        return redirect('home')  # Sau khi xóa, quay về trang chủ
    else:
        return render(request, 'posts/forbidden.html', status=403)  # Trả về lỗi 403 nếu không có quyền

def manage_blog(request):
    return render(request, 'posts/manage_blog.html')

def logout_view(request):
    logout(request)
    return render(request, 'posts/home.html') # Chuyển hướng về trang chủ sau khi logout

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Đăng nhập user
            return redirect('post')  # Chuyển hướng về 
    return render(request, 'login.html')