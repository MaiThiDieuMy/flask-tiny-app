from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth import logout,login
from django.contrib import messages

def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})
def post_list(request):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')  # Lấy từ khóa tìm kiếm (mặc định là rỗng)
        
        if query:
            posts_list = Post.objects.filter(title__icontains=query).order_by('-id')
        else:
            posts_list = Post.objects.all().order_by('-id')

        paginator = Paginator(posts_list, 5)  # Hiển thị 5 bài viết mỗi trang
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        return render(request, 'posts/post.html', {'posts': posts, 'query': query})

    else:
        return render(request, 'posts/home.html')  # Chuyển hướng về home nếu chưa đăng nhập

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

# Hiển thị chi tiết bài viết
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Lấy tất cả bình luận
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments})

# Thêm bình luận khi nhấn nút ➜
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text.strip():
            Comment.objects.create(post=post, user=request.user, content=comment_text)  # Đổi author -> user
    return redirect('post_detail', post_id=post_id)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Chỉ cho phép tác giả bài viết hoặc admin xóa
    if request.user == post.author or request.user.is_superuser:
        post.delete()
    return redirect('post_list')  # Sau khi xóa, quay về trang chủ

# Xóa bài viết đã chọn
def delete_selected_posts(request):
    if request.method == "POST":
        selected_posts = request.POST.getlist('selected_posts')

        # Kiểm tra xem có bài viết nào được chọn hay không
        if selected_posts:
            posts = Post.objects.filter(id__in=selected_posts, author=request.user)
            posts.delete()
            messages.success(request, "Đã xóa các bài viết đã chọn.")
        else:
            messages.error(request, "Bạn chưa chọn bài viết nào để xóa.")

    return redirect('manage_blog')
   

# def manage_blog(request):
#     return render(request, 'posts/manage_blog.html')

# Quản lý các bài viết của người dùng
def manage_blog(request):
    # Lấy tất cả bài viết của người dùng hiện tại
    posts = Post.objects.filter(author=request.user)  # Lọc các bài viết của tác giả hiện tại
    return render(request, 'posts/manage_blog.html', {'posts': posts})


def logout_view(request):
    logout(request)
    return render(request, 'posts/home.html') # Chuyển hướng về trang chủ sau khi logout

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)  # Đăng nhập user
#             return redirect('post')  # Chuyển hướng về 
#     return render(request, 'login.html')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Kiểm tra quyền chỉnh sửa (chỉ tác giả mới được chỉnh sửa)
    if request.user != post.author:
        return redirect('post_detail', post_id=post_id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'posts/edit_post.html', {'post': post})