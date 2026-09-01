from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL_USER: str = ""
    EMAIL_PASSWORD: str = ""
    GOOGLE_AI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.7-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()