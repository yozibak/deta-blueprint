from pydantic import BaseSettings

class Settings(BaseSettings):
    uc: str

    class Config:
        env_file = ".env"