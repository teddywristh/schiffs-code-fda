# Cài đặt dự án

## Môi trường developer

Vì toàn bộ cấu hình đã được thiết lập, chỉ cần tạo một file `.env` theo `.env.example` và thay đổi một vài biến là có thể chạy được dự án

1. Copy file `.env.example` thành `.env`
2. Chỉnh sửa một vài biến môi trường sau:
- `COMPOSE_PROJECT_NAME`: Đây là tên cả container, giữ nguyên hoặc đặt tên khác nếu có container khác có tên này rồi.
- Cấu hìn cổng cho dự án: Các cổng ở đây lưu ý là chưa được sử dụng bởi một container nào trong docker nếu không thì sẽ bị xung đột
- DATABASE: sửa mỗi password là được
- `SECRET_KEY`: đổi key cho jwt để không bị lộ

Sau khi hoàn thành việc thiết lập biến môi trường, có thể sử dụng `docker copmose up --build` để kiểm tra xem dự án đã chạy được chưa