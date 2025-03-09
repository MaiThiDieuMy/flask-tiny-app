# Chọn image Python chính thức từ Docker Hub
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tệp requirements.txt vào container
COPY requirements.txt /app/

# Nâng cấp pip và cài đặt các phụ thuộc từ requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn của ứng dụng vào container
COPY . /app/

# Mở cổng mà ứng dụng sẽ chạy trên container
EXPOSE 8000

# Khởi động ứng dụng Django khi container chạy
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
