from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    debug: bool = False
    azure_storage_connection_string: str = ""
    azure_storage_queue_name: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
