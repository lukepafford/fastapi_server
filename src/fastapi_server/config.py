from pydantic import BaseSettings


class Settings(BaseSettings):
    github_secret: str
    tower_url: str
    tower_token: str

    class Config:
        env_file = ".env"


settings = Settings()
