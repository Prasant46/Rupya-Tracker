import os

class BaseConfig:
  SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
  CORS_ALLOWED_ORIGINS = os.getenv("FRONTEND_URL", "http://localhost:3000")
  FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
  
  # JWT Cookie settings
  JWT_TOKEN_LOCATION = ["cookies"]
  JWT_COOKIE_SECURE = False  
  JWT_COOKIE_CSRF_PROTECT = False  
  JWT_ACCESS_COOKIE_PATH = "/"
  JWT_COOKIE_SAMESITE = "Lax"
  
  JWT_ERROR_MESSAGE_KEY = "message"
  
  # OAuth settings
  GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
  GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
  GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
  GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
  
class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_COOKIE_SECURE = True

class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/expanse_tracker")

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return ProdConfig if env == "production" else DevConfig
    