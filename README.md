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
| **Media (MinIO)** | MinIO Object Storage | `http://localhost:9000` (API)<br>`http://localhost:9001` (Console) | Lưu trữ riêng tư ảnh và âm thanh; truy cập bằng URL ký hạn |
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

Trước khi khởi động, đặt `SECRET_KEY` trong file `.env` ở thư mục gốc bằng
một giá trị ngẫu nhiên riêng (không dùng secret mẫu). Có thể tạo bằng lệnh:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

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
  - Bucket mặc định: `kidspeak-media` (tự động khởi tạo ở chế độ private)

### Quản lý nội dung học tập (Expert)

Đăng nhập trả JWT Bearer token; `/api/auth/me` xác minh phiên và trả role hiện tại
từ database. Các API quản lý danh mục và bài học yêu cầu role `EXPERT` hoặc `ADMIN`:

- `/api/lesson-categories`: CRUD danh mục, danh sách có phân trang.
- `/api/lessons`: CRUD bài học; hỗ trợ lọc theo danh mục, mức độ, trạng thái xuất bản và tìm kiếm.
- Ảnh được gửi bằng `multipart/form-data`, lưu trên MinIO và trả về dưới dạng URL có chữ ký.

Trước khi chạy migration do dự án quản lý, kiểm tra các cột mới trong model:
`lesson_categories.image`, `lesson_categories.updated_at`, và `lessons.image`.
Backend không tự tạo hoặc chạy migration.

Các khu vực `/student`, `/expert` và `/admin` yêu cầu đăng nhập và chỉ cho phép
role tương ứng. Role DB hiện tên `USER` được chuẩn hóa thành `STUDENT` trong auth
response/JWT; phân quyền backend luôn dựa trên role hiện tại trong database.

Backend dùng `MediaStorageService` để kiểm tra định dạng và dung lượng trước khi lưu.
Ảnh đại diện được lưu dưới dạng object key trong `users.avatar`; trình duyệt nhận
presigned URL có thời hạn, không lưu URL này vào database. URL MinIO được ký cho
trình duyệt qua `MINIO_PUBLIC_ENDPOINT` (mặc định `localhost:9000`), còn backend
trong Docker kết nối MinIO nội bộ qua `media:9000`.
MinIO trả nội dung qua presigned `GET` URL và hỗ trợ HTTP Range để audio có thể
phát/tua theo khả năng của trình duyệt.

Các biến media có thể cấu hình trong `.env`:

- `MINIO_ENDPOINT` / `MINIO_PUBLIC_ENDPOINT`: endpoint backend và endpoint trình duyệt.
- `MEDIA_URL_EXPIRY_SECONDS`: thời hạn presigned URL (mặc định 1800 giây).
- `MEDIA_IMAGE_MAX_BYTES`: dung lượng ảnh tối đa (mặc định 5 MiB).
- `MEDIA_AUDIO_MAX_BYTES`: dung lượng audio tối đa (mặc định 25 MiB).

Các endpoint avatar yêu cầu Bearer token: `POST /api/media/avatar` (multipart field
`file`), `GET /api/media/avatar` lấy URL mới, và `DELETE /api/media/avatar`.
Service nền tảng cũng hỗ trợ JPG/JPEG, PNG, WebP, MP3, WAV, M4A, OGG và WebM.

### 5. Chạy AI app trực tiếp bằng Python và test Swagger
Chạy từ thư mục `ai/app` (nếu cổng `8001` đang được Docker AI service sử dụng, hãy dừng service đó trước):

```powershell
cd ai\app
python main.py
```

Mở [http://localhost:8001/docs](http://localhost:8001/docs), chọn `POST /analyze` → **Try it out**, nhập `tu_chuan`, chọn file ghi âm tại `audio`, rồi nhấn **Execute**. Kết quả trả về gồm điểm và chi tiết lỗi phát âm. Cần nhập `tu_chuan` để hệ thống biết từ chuẩn cần so sánh.

### 6. Xem logs
```bash
# Xem logs toàn bộ hệ thống
docker compose logs -f

# Xem logs của từng dịch vụ cụ thể
docker compose logs -f backend
docker compose logs -f ai
docker compose logs -f media
docker compose logs -f frontend
```

### 7. Dừng hệ thống
```bash
# Dừng các container
docker compose down

# Dừng và xóa toàn bộ dữ liệu database & media nếu muốn reset sạch
docker compose down -v
```

# Hướng dẫn sử dụng tone màu dự án
Tạo Login View cho Actor trẻ em bằng Vue 3 + Vite + Tailwind CSS.

Yêu cầu:
- Sử dụng bảng màu khai báo bằng `@theme` trong `frontend/src/style.css`.
- Background: `bg-kids-bg`.
- Login card: `bg-kids-surface`.
- Màu chủ đạo: `text-kids-text`.
- Các chi tiết nổi bật: `bg-kids-primary`, `bg-kids-secondary`.
- Nút đăng nhập: `bg-kids-cta`.
- Thiết kế thân thiện, vui nhộn, phù hợp với trẻ em.
- Card bo góc lớn, shadow nhẹ, khoảng cách thoáng.
- Responsive trên desktop và mobile.
- Không hardcode mã HEX trong component.
- Tái sử dụng các component hiện có nếu phù hợp.

Tạo Login View cho Actor Giảng viên và Admin bằng Vue 3 + Vite + Tailwind CSS.

Yêu cầu:
- Sử dụng bảng màu khai báo bằng `@theme` trong `frontend/src/style.css`.
- Background: `bg-admin-bg`.
- Login card: `bg-admin-surface`.
- Primary: `bg-admin-primary`.
- Secondary: `text-admin-secondary`.
- CTA Button: `bg-admin-cta`.
- Text: `text-admin-text`.
- Thiết kế chuyên nghiệp, hiện đại, tối giản theo phong cách SaaS Dashboard.
- Responsive trên desktop và mobile.
- Không hardcode mã HEX trong component.
- Tái sử dụng các component hiện có nếu phù hợp.

Các utility feedback dùng chung: `text-feedback-success`, `text-feedback-warning`,
`text-feedback-error` và `text-feedback-info` (có thể dùng các tiền tố màu khác
như `bg-` hoặc `border-`).