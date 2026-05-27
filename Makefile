# --- ĐỊNH NGHĨA CÁC BIẾN MÔI TRƯỜNG ---
COMPOSE_BASE = docker compose -f docker-compose.yml
COMPOSE_DEV  = docker compose
COMPOSE_PROD = $(COMPOSE_BASE) -f docker-compose.prod.yml

# Bổ sung các lệnh logs lẻ vào danh sách .PHONY
.PHONY: dev dev-down dev-refresh prod prod-down logs-dev logs-prod logs-backend logs-frontend logs-db ps clean db-migrate db-upgrade

# ==========================================
# MÔI TRƯỜNG DEV (LÚC CODE)
# ==========================================

dev:
	$(COMPOSE_DEV) up -d --build

dev-down:
	$(COMPOSE_DEV) down

dev-refresh:
	$(COMPOSE_DEV) down --remove-orphans
	$(COMPOSE_DEV) up -d --build --force-recreate --remove-orphans

# ==========================================
# MÔI TRƯỜNG PROD (LÚC LÊN SERVER)
# ==========================================

prod:
	$(COMPOSE_PROD) up -d --build

prod-down:
	$(COMPOSE_PROD) down

# ==========================================
# CÔNG CỤ TIỆN ÍCH (LOGS & QUẢN LÝ)
# ==========================================

# Xem toàn bộ log của môi trường Dev (Tất cả dịch vụ trộn lẫn)
logs-dev:
	$(COMPOSE_DEV) logs -f

# Xem toàn bộ log của môi trường Prod
logs-prod:
	$(COMPOSE_PROD) logs -f

# --- CÁC LỆNH XEM LOG LẺ TỪNG DỊCH VỤ (MÔI TRƯỜNG DEV) ---

# Chỉ xem log của Backend (FastAPI)
logs-backend:
	$(COMPOSE_DEV) logs -f backend

# Chỉ xem log của Frontend (Vite/React)
logs-frontend:
	$(COMPOSE_DEV) logs -f frontend

# Chỉ xem log của Database (PostgreSQL)
logs-db:
	$(COMPOSE_DEV) logs -f db-postgre

# ==========================================

# Xem danh sách các container đang chạy ở Dev
ps:
	$(COMPOSE_DEV) ps

# ==========================================
# CÁC LỆNH QUẢN LÝ DATABASE (ALEMBIC)
# ==========================================

# Tạo file migration mới (Yêu cầu điền message. Ví dụ: make db-migrate msg="Thêm bảng user")
db-migrate:
	@if [ -z "$(msg)" ]; then \
		echo "Lỗi: Vui lòng nhập nội dung thay đổi. Cú pháp: make db-migrate msg=\"nội dung\""; \
	else \
		$(COMPOSE_DEV) exec backend alembic revision --autogenerate -m "$(msg)"; \
	fi

# Cập nhật Database lên phiên bản mới nhất (Áp dụng migration)
db-upgrade:
	$(COMPOSE_DEV) exec backend alembic upgrade head

# ==========================================

# Dọn dẹp sạch sẽ toàn bộ (Xóa cả database volume của Dev) - Dùng cẩn thận
clean:
	$(COMPOSE_DEV) down --volumes --remove-orphans