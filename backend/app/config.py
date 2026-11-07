from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GetClient"
    environment: str = "development"
    debug: bool = True
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/getclient"
    allowed_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    auth_token_secret: SecretStr = SecretStr("development-only-token-secret-change-before-deploy")
    access_token_expire_minutes: int = 30

    @model_validator(mode="after")
    def validate_auth_token_secret(self) -> "Settings":
        secret = self.auth_token_secret.get_secret_value()
        if self.access_token_expire_minutes <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be greater than zero")
        if len(secret.encode()) < 32:
            raise ValueError("AUTH_TOKEN_SECRET must be at least 32 bytes")
        if self.environment.lower() == "production" and secret.startswith("development-only-"):
            raise ValueError("AUTH_TOKEN_SECRET must be set to a unique production secret")
        return self

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
