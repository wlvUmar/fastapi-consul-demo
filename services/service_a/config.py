from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "Service A"
    service_id: str = "service-a"
    host: str = "127.0.0.1"
    port: int = 8001
    service_address: str = "127.0.0.1"
    consul_host: str = "127.0.0.1"
    consul_port: int = 8500


settings = Settings()
