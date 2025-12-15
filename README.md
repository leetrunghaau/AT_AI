# Hệ thống Nhận dạng Khuôn mặt

Đây là một dự án API nhận dạng khuôn mặt sử dụng mô hình **AuraFace-v1**. API được xây dựng bằng FastAPI và sử dụng Faiss để tìm kiếm vector hiệu suất cao.

## Chức năng

- **Đăng ký (`/register`)**: Đăng ký một người dùng mới bằng cách cung cấp một hoặc nhiều hình ảnh và `user_id`. Hệ thống sẽ trích xuất các vector đặc trưng khuôn mặt, tính giá trị trung bình và lưu vào cơ sở dữ liệu.
- **Nhận dạng (`/recognize`)**: Tìm kiếm một khuôn mặt trong cơ sở dữ liệu. Hệ thống sẽ trả về `user_id` và khoảng cách (mức độ tương đồng) nếu tìm thấy.

## Cấu trúc dự án

```
.
├── align/         # Chứa code để căn chỉnh khuôn mặt
├── database/      # Quản lý cơ sở dữ liệu vector Faiss
├── embeddings/    # Trích xuất vector đặc trưng từ khuôn mặt
├── models/        # Chứa các file của mô hình ONNX
├── face_service.py # File chính, định nghĩa các API endpoint
├── service.py     # Lớp logic nghiệp vụ chính
└── README.md
```

## Hướng dẫn cài đặt

### 1. Tải mô hình

Mô hình nhận dạng khuôn mặt **AuraFace-v1** không được bao gồm trong repository này do kích thước lớn. Bạn cần tải nó về thủ công.

- **Nguồn**: [https://huggingface.co/fal/AuraFace-v1/tree/main](https://huggingface.co/fal/AuraFace-v1/tree/main)
- **Tải xuống**: Tải tất cả các file `.onnx` từ link trên.
- **Lưu trữ**: Tạo thư mục `models/AuraFace-v1/` và đặt các file đã tải vào đó. Cấu trúc cuối cùng sẽ trông như sau:
  ```
  models/
  └── AuraFace-v1/
      ├── 1k3d68.onnx
      ├── 2d106det.onnx
      ├── genderage.onnx
      ├── glintr100.onnx
      └── scrfd_10g_bnkps.onnx
  ```

### 2. Cài đặt thư viện Python

Dự án yêu cầu các thư viện Python sau. Bạn nên tạo một môi trường ảo (virtual environment) để quản lý chúng.

Tạo và lưu các thư viện sau vào file `requirements.txt`:
```txt
fastapi
uvicorn[standard]
python-multipart
opencv-python
numpy
faiss-cpu
onnxruntime
```

Sau đó, cài đặt bằng pip:
```bash
pip install -r requirements.txt
```
*Lưu ý: `faiss-cpu` dành cho máy chỉ có CPU. Nếu bạn có GPU và CUDA được cài đặt, bạn có thể cài `faiss-gpu` để có hiệu suất tốt hơn.*

### 3. Chạy ứng dụng

Sử dụng uvicorn để khởi động server API:
```bash
uvicorn face_service:app --host 0.0.0.0 --port 8000
```
Server sẽ chạy tại `http://localhost:8000`.

## Hướng dẫn sử dụng API

Bạn có thể sử dụng các công cụ như `curl` hoặc Postman để tương tác với API.

### Đăng ký (`/register`)

- **Endpoint**: `POST /register`
- **Mô tả**: Đăng ký một `user_id` mới với một hoặc nhiều ảnh.
- **Parameters** (`multipart/form-data`):
  - `user_id` (str): ID định danh cho người dùng.
  - `files` (List[UploadFile]): Một hoặc nhiều file ảnh.
  - `landmarks` (str): Một chuỗi JSON chứa danh sách các mốc khuôn mặt (landmarks) cho mỗi ảnh. Mỗi landmark là một danh sách 5 cặp tọa độ `[x, y]` đã được chuẩn hóa (giá trị từ 0 đến 1).

**Ví dụ với `curl`:**
```bash
curl -X POST "http://localhost:8000/register" \
-F "user_id=user_01" \
-F "files=@/path/to/image1.jpg" \
-F "files=@/path/to/image2.png" \
-F 'landmarks=[[[0.38, 0.51], [0.73, 0.51], [0.56, 0.71], [0.41, 0.92], [0.70, 0.92]], [[0.39, 0.52], [0.74, 0.52], [0.57, 0.72], [0.42, 0.93], [0.71, 0.93]]]' 
```

### Nhận dạng (`/recognize`)

- **Endpoint**: `POST /recognize`
- **Mô tả**: Nhận dạng một người từ một ảnh.
- **Parameters** (`multipart/form-data`):
  - `file` (UploadFile): Một file ảnh.
  - `landmarks` (str): Một chuỗi JSON chứa các mốc khuôn mặt cho ảnh.

**Ví dụ với `curl`:**
```bash
curl -X POST "http://localhost:8000/recognize" \
-F "file=@/path/to/unknown_person.jpg" \
-F 'landmarks=[[0.38, 0.51], [0.73, 0.51], [0.56, 0.71], [0.41, 0.92], [0.70, 0.92]]'
```

- **Kết quả thành công**:
  ```json
  {
    "user_id": "user_01",
    "distance": 0.2345
  }
  ```
- **Kết quả không tìm thấy**:
  ```json
  {
    "user_id": null,
    "distance": null
  }
  ```

```