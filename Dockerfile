# Sử dụng base image Python 3.10-slim để tối ưu kích thước
FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết cho OpenCV
# Giúp hình ảnh headless (không có giao diện đồ họa) hoạt động ổn định
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file requirements.txt và cài đặt các thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của dự án vào thư mục làm việc trong container
# Thao tác này sẽ bao gồm cả thư mục `models` mà bạn đã tải về
COPY . .

# Mở cổng 8000 để cho phép truy cập từ bên ngoài container
EXPOSE 8000

# Lệnh để khởi chạy ứng dụng khi container bắt đầu
# Chạy uvicorn và cho phép truy cập từ mọi địa chỉ IP
CMD ["uvicorn", "face_service:app", "--host", "0.0.0.0", "--port", "8000"]
