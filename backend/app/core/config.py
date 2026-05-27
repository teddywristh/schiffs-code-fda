from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. Cấu hình API chung
    PROJECT_NAME: str
    API_V1_STR: str

    # 2. Cấu hình Bảo mật (JWT)
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 3. Cấu hình kết nối Cơ sở dữ liệu
    DATABASE_URL: str

    # Chỉ định cấu hình để Pydantic đọc file .env
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Khởi tạo một đối tượng settings duy nhất để dùng chung cho toàn bộ hệ thống Backend
settings = Settings()