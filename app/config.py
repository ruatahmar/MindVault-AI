from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: int  
    JWT_ALGORITHM: str
    RESET_TOKEN_SECRET_KEY: str

    DATABASE_URL: str
    GEMINI_API_KEY: str

    EMAIL:str
    EMAIL_APP_PASSWORD:str

    class Config:
        env_file = ".env"

settings = Settings()
