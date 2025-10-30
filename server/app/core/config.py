from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "interview_db"
    REDIS_URL: str = "redis://localhost:6379"
    PORT: int = 4000
    ENV: str = "dev"
    SECRET_KEY: str = "dev-secret-change-in-production-use-32-bytes-min"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()

