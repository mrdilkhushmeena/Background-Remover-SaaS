import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    DB_NAME = "tools.db"