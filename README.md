# 📌 Project: blog

---

## 👥 Thông tin thành viên
- **Mai Thị Diệu My** - `22707221`

---

## 📖 Giới thiệu
**Blog** 

---

## 🚀 Hướng dẫn cài đặt và chạy ứng dụng

## 🚀 Cách 1:

### 1️⃣ **Clone repository**
Mở terminal hoặc command prompt và chạy lệnh:
```sh
 git clone https://github.com/MaiThiDieuMy/flask-tiny-app
```

### 2️⃣ **Di chuyển vào thư mục dự án**
```sh
 cd flask-tiny-app
```

### 3️⃣ **Tạo môi trường ảo (`venv`)**
```sh
 python -m venv venv
```

### 4️⃣ **Kích hoạt môi trường ảo**
- **Windows:**
  ```sh
  ./venv/Scripts/Activate.ps1
  ```
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

### 5️⃣ **Cài đặt dependencies**
```sh
 pip install -r requirements.txt
```

### 6️⃣ **Thiết lập database**
```sh
 python manage.py makemigrations
 python manage.py migrate
```

### 7️⃣ **Chạy ứng dụng**
```sh
 python manage.py runserver
```

Sau đó, mở trình duyệt và truy cập **[http://127.0.0.1:8000](http://127.0.0.1:8000)** để sử dụng ứng dụng.

## 🚀 Cách 2: Chạy trên Docker

### 1️⃣ **Clone repository**
Mở terminal hoặc command prompt và chạy lệnh:
```sh
 git clone https://github.com/MaiThiDieuMy/flask-tiny-app.git
```
### 2️⃣ **Di chuyển vào thư mục dự án**
```sh
 cd flask-tiny-app
```
### 3️⃣ **Đóng gói**
Mở terminal hoặc command prompt và chạy lệnh, bước này sẽ khởi tạo images:
```sh
 docker-compose build 
```
Sau đó chạy lệnh:
```sh
 docker-compose up
```
Để khởi tạo container.
### 4️⃣ **Vào container bằng cách**
```sh
 docker ps
 docker exec -it <container_id> bash
 python manage.py makemigrations
 python manage.py migrate
```
### 5️⃣ **Chạy ứng dụng**
Nhấn chuột vào ports 8000:8000

