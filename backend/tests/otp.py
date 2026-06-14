"""
Kiểm tra hệ thống gửi mã OTP từ tài khoản hệ thống tới các tài khoản email khác
"""
from pathlib import Path
import sys
import asyncio

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.helper.otp import send_email

async def main():
    receiver_email = "nguyentrongdai1506@gmail.com"
    otp_code = "123456"
    
    print("Bắt đầu thử nghiệm gửi OTP xác thực tài khoản...")
    try:
        await send_email(email=receiver_email, otp=otp_code)
        print("Gửi email xác thực thành công!")
    except Exception as e:
        print("Lỗi khi gửi email xác thực:", e)

if __name__ == "__main__":
    asyncio.run(main())