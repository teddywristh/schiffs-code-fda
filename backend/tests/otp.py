"""
Kiểm tra hệ thống gửi mã OTP từ tài khoản hệ thống tới các tài khoản emai khác

Yêu cầu:
- Tài khoản email và mật khẩu sẽ được lấy từ file .env
"""
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import smtplib
from email.mime.text import MIMEText

from app.core.config import settings

# 1. Thông tin tài khoản
sender_email = settings.ADMIN_USERNAME
sender_password = settings.EMAIL_PASSWORD
receiver_email = "nguyentrongdai1506@gmail.com"

body = """
Xin chào,

Mã OTP của bạn là: 482731

Mã có hiệu lực trong 5 phút.

Nếu bạn không thực hiện yêu cầu này, hãy bỏ qua email.

Trân trọng,
Đội ngũ MyApp
"""

message = MIMEText(body)
message["Subject"] = "Welcome to Schiffs Code FDA"
message["From"] = f"Schiffs Code FDA <{sender_email}>"
message["To"] = receiver_email

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_email, sender_password)

    server.send_message(message)

    server.quit()

    print("Gửi email thành công!")

except Exception as e:
    print("Lỗi:", e)