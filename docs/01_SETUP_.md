# Hướng dẫn cài đặt lần đầu

Tài liệu này hướng dẫn cách thiết lập dự án từ đầu để chạy được cả khi dùng Docker Compose lẫn khi mở bằng devcontainer.

## 1. Yêu cầu trước khi bắt đầu

Bạn cần cài sẵn các công cụ sau:

- Docker Engine / Docker Desktop
- Docker Compose
- VS Code
- Extension `Dev Containers` trong VS Code nếu muốn làm việc trong container

## 2. Sao chép file cấu hình môi trường

Trong dự án đã có sẵn file mẫu là `.env.example`. Ở lần đầu tiên, hãy tạo file `.env` ở thư mục gốc của project bằng cách sao chép từ file mẫu.

```bash
cp .env.example .env
```

## 3. Chỉnh sửa file `.env`

File `.env` dùng chung cho Docker Compose, devcontainer và backend. Bạn chỉ cần chỉnh một vài biến quan trọng sau:

- `COMPOSE_PROJECT_NAME`: tên của project trong Docker Compose. Có thể giữ nguyên hoặc đổi nếu máy bạn đã có project khác trùng tên.
- `HOST_PORT_FRONTEND`: cổng frontend trên máy host.
- `HOST_PORT_BACKEND`: cổng backend trên máy host.
- `HOST_PORT_DB`: cổng PostgreSQL trên máy host.
- `POSTGRES_PASSWORD`: mật khẩu PostgreSQL, nên đổi trước khi chạy thật.
- `SECRET_KEY`: khóa bí mật dùng cho JWT, bắt buộc nên đổi.
- `ADMIN_USERNAME` và `ADMIN_PASSWORD`: tài khoản admin mặc định khi hệ thống khởi tạo.

Ví dụ cấu hình:

```env
COMPOSE_PROJECT_NAME=schiffs-code-fda
HOST_PORT_FRONTEND=3001
HOST_PORT_BACKEND=8001
HOST_PORT_DB=5433

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_strong_password
POSTGRES_DB=db-schiffs

SECRET_KEY=your_super_secret_key
ADMIN_USERNAME=admin@system.com
ADMIN_PASSWORD=your_admin_password
```

### Lưu ý về database

- Khi chạy trên máy local bằng Docker Compose, dịch vụ backend sẽ kết nối PostgreSQL qua `DATABASE_URL` được compose inject sẵn.
- Khi chạy trong devcontainer `workspace`, file compose của devcontainer cũng đã inject `DATABASE_URL` trỏ về service `db-postgre`.
- Nếu bạn chạy code trực tiếp ngoài Docker, backend sẽ fallback về `localhost` và dùng `HOST_PORT_DB` trong `.env`.
- Nếu trước đó bạn đã khởi động dự án rồi và muốn setup lại từ đầu, hãy xóa container và volume PostgreSQL cũ để dữ liệu và schema được tạo mới đúng cấu hình.

```bash
docker compose down -v
```

Sau đó hãy chạy lại `docker compose up --build`.

## 4. Chạy dự án bằng Docker Compose

Sau khi đã có file `.env`, bạn có thể khởi động toàn bộ hệ thống bằng lệnh:

```bash
docker compose up --build
```

Lệnh này sẽ khởi động:

- PostgreSQL
- Backend FastAPI
- Frontend

## 5. Chạy trong devcontainer

Nếu bạn muốn làm việc trực tiếp trong VS Code Dev Containers, hãy mở cấu hình ở thư mục:

`.devcontainer/fullstack`

Khi mở container lần đầu, devcontainer sẽ:

- tự tạo `.env` nếu chưa có
- cài package Python ở `backend`
- cài package Node.js ở `frontend`
- chạy các service cần thiết trong Docker Compose

Nếu bạn vừa thay đổi `.env` hoặc sửa cấu hình Docker Compose, hãy chọn:

```text
Dev Containers: Rebuild and Reopen in Container
```

## 6. Kiểm tra migration database

Sau khi database đã chạy, bạn có thể chạy migration bằng Alembic.

### Khi làm việc trong devcontainer

Mở terminal trong devcontainer rồi chạy:

```bash
cd /workspace/backend
alembic upgrade head
```

### Khi chạy local ngoài Docker

Vào thư mục `backend` rồi chạy:

```bash
cd backend
alembic upgrade head
```

## 7. Kiểm tra backend hoạt động

Sau khi khởi động xong, bạn có thể kiểm tra nhanh:

- API gốc: `http://localhost:8001/`
- Health check: `http://localhost:8001/health`

Nếu backend chạy đúng, endpoint `/health` sẽ trả về trạng thái kết nối database thành công.

## 8. Một vài lỗi thường gặp

### 8.1 Lỗi không kết nối được PostgreSQL

Nguyên nhân thường gặp:

- PostgreSQL chưa chạy
- `HOST_PORT_DB` bị trùng với cổng khác trên máy
- bạn đang chạy lệnh ở sai môi trường, ví dụ chạy trong `workspace` nhưng lại dùng URL của local host

### 8.2 Chạy `alembic` nhưng báo không thấy `DATABASE_URL`

Nếu bạn đang dùng devcontainer, hãy đảm bảo đã rebuild container sau khi sửa compose hoặc `.env`.

### 8.3 Thay đổi `.env` nhưng ứng dụng chưa nhận cấu hình mới

Docker Compose và devcontainer chỉ đọc biến môi trường lúc container được tạo. Sau khi sửa `.env`, bạn nên khởi động lại hoặc rebuild container để nhận giá trị mới.

## 9. Tóm tắt nhanh

1. Copy `.env.example` thành `.env`
2. Chỉnh các biến quan trọng như mật khẩu DB, `SECRET_KEY`, cổng chạy
3. Chạy `docker compose up --build`
4. Nếu dùng devcontainer thì mở `.devcontainer/fullstack`
5. Chạy `alembic upgrade head` để tạo/đồng bộ schema

Sau khi hoàn thành các bước trên, project có thể chạy ổn định ở cả môi trường local lẫn devcontainer.

## 10. Lưu ý khi đã từng chạy dự án trước đó

Nếu bạn đã khởi động dự án trước đó thì hãy xóa dữ liệu PostgreSQL cũ rồi chạy lại từ đầu để tránh bị kẹt ở schema hoặc revision cũ. Do ở cập nhật mới nhất tôi đã gộp 2 file alembic để clean code, vì vậy việc tạo bảng 2 lần ở versions đầu tiên sẽ khiến lỗi, tốt nhất là xóa postgre container đi và khởi động lại.

```bash
docker compose down db-postgre -v
docker compose up db-postgre --build
```

Sau đó chạy lại migration:

```bash
cd backend
alembic upgrade head
```