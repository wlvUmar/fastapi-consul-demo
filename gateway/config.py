from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    host: str = "127.0.0.1"
    port: int = 8000
    service_a_url: str = "http://localhost:8001"
    service_b_url: str = "http://localhost:8002"
    service_c_url: str = "http://localhost:8003"
    request_timeout: float = 5.0


settings = Settings()
