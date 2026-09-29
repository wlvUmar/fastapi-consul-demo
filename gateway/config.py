from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    host: str = "127.0.0.1"
    port: int = 8000
    consul_host: str = "127.0.0.1"
    consul_port: int = 8500
    request_timeout: float = 5.0


settings = Settings()
