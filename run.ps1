# Đặt chính sách thực thi PowerShell để chạy các script
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue

# Tìm và sử dụng Python
$pythonCommand = "python"

# Xóa và tạo lại môi trường ảo
Remove-Item -Recurse -Force .\venv -ErrorAction SilentlyContinue
Write-Host "Đang tạo môi trường ảo..." -ForegroundColor Green
& $pythonCommand -m venv venv

# Kích hoạt môi trường ảo
Write-Host "Đang kích hoạt môi trường ảo..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Nâng cấp pip và cài đặt các thư viện từ requirements.txt
Write-Host "Đang nâng cấp pip và cài đặt các thư viện..." -ForegroundColor Green
& $pythonCommand -m pip install --upgrade pip
& $pythonCommand -m pip install -r requirements.txt

# Khởi tạo cơ sở dữ liệu (nếu cần thiết cho Django)
Write-Host "Đang khởi tạo cơ sở dữ liệu..." -ForegroundColor Green
& $pythonCommand manage.py migrate

Write-Host "Cài đặt hoàn tất thành công!" -ForegroundColor Green
Write-Host "Đang khởi động ứng dụng Django..." -ForegroundColor Cyan

# Khởi động ứng dụng Django
Start-Process "python" -ArgumentList "manage.py runserver"

Write-Host "
Thông tin đăng nhập mặc định:
Tên người dùng: maimy
Mật khẩu: 123456
" -ForegroundColor Cyan

# Mở trình duyệt mặc định
Start-Process "http://127.0.0.1:8000"
.\run.ps1
