# KidSpeak 🎙️👶
AI-powered Vietnamese pronunciation learning platform for children, providing speech recognition, pronunciation assessment, and personalized feedback.

---

## 🏗️ Kiến trúc Hệ thống (System Architecture)

Hệ thống được đóng gói hoàn chỉnh bằng Docker Compose gồm 5 thành phần chính:

| Dịch vụ (Service) | Công nghệ | Cổng (Port) | Chức năng |
| :--- | :--- | :--- | :--- |
| **Frontend** | Vue 3 + Vite | `http://localhost:5173` | Giao diện học tập cho trẻ em và phụ huynh |
| **Backend** | FastAPI (Python) | `http://localhost:8000` | Quản lý nghiệp vụ, API, xác thực, bài học (`/docs`) |
| **AI Service** | FastAPI + PyTorch/FFmpeg | `http://localhost:8001` | Nhận diện giọng nói, thẩm định & chấm điểm phát âm (`/docs`) |
| **Media (MinIO)** | MinIO Object Storage | `http://localhost:9000` (API)<br>`http://localhost:9001` (Console) | Lưu trữ file âm thanh mẫu, bản ghi âm của trẻ, media bài học |
| **Database** | PostgreSQL 16 | `localhost:5432` | Cơ sở dữ liệu chính của hệ thống |

---

## 🚀 Hướng dẫn Chạy với Docker

### 1. Chuẩn bị môi trường
Đảm bảo máy đã cài đặt **Docker Desktop** và đang chạy.

File cấu hình `.env` ở thư mục gốc đã được thiết lập sẵn các giá trị mặc định. Bạn có thể kiểm tra hoặc điều chỉnh nếu cần:
- `MINIO_ROOT_USER`: `minioadmin`
- `MINIO_ROOT_PASSWORD`: `minioadmin`
- `DB_USER`: `postgres`
- `DB_PASSWORD`: `kidspeak_password`

### 2. Khởi động toàn bộ hệ thống
Tại thư mục gốc dự án (`sourecode`), chạy lệnh sau:

```bash
docker compose up -d --build
```

### 3. Kiểm tra trạng thái các dịch vụ
```bash
docker compose ps
```

### 4. Truy cập các dịch vụ
- **Giao diện Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **AI Service API & Docs**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **MinIO Web Console (Quản lý File Audio & Media)**: [http://localhost:9001](http://localhost:9001)
  - Tên đăng nhập: `minioadmin`
  - Mật khẩu: `minioadmin`
  - Bucket mặc định: `kidspeak-media` (tự động khởi tạo và phân quyền tải file)

### 5. Xem logs
```bash
# Xem logs toàn bộ hệ thống
docker compose logs -f

# Xem logs của từng dịch vụ cụ thể
docker compose logs -f backend
docker compose logs -f ai
docker compose logs -f media
docker compose logs -f frontend
```

### 6. Dừng hệ thống
```bash
# Dừng các container
docker compose down

# Dừng và xóa toàn bộ dữ liệu database & media nếu muốn reset sạch
docker compose down -v
```
