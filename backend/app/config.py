import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database Configuration
    oracle_user: str = os.getenv("ORACLE_USER", "system")
    oracle_password: str = os.getenv("ORACLE_PASSWORD", "bhavyaoracle")
    oracle_host: str = os.getenv("ORACLE_HOST", "localhost")
    oracle_port: int = int(os.getenv("ORACLE_PORT", 1521))
    oracle_service: str = os.getenv("ORACLE_SERVICE", "XE")
    oracle_client_lib_dir: str = os.getenv(
        "ORACLE_CLIENT_LIB_DIR", 
        r"C:\wipro_labs\instantclient-basic-windows.x64-23.26.2.0.0\instantclient_23_0"
    )
    
    # Security Configuration
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_hours: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 2))
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    
    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # AI/LLM Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Server Configuration
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", 8000))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        """Pydantic v2 configuration"""
        env_file = str(Path(__file__).resolve().parent.parent / ".env")
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
