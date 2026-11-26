from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    TOKEN_RENEW_BEFORE_MINUTES: int = 15
    TOKEN_ABSOLUTE_MAX_HOURS: int = 8
    EMAIL_USER: str = ""
    EMAIL_PASSWORD: str = ""
    GOOGLE_AI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.7-flash"
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [origen.strip() for origen in self.CORS_ORIGINS.split(",") if origen.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()