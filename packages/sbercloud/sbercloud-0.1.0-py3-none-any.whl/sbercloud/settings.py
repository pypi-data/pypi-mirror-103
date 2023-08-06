from pydantic import BaseSettings


class Settings(BaseSettings):
    domain: str
    username: str
    password: str
    project_id: str
    region: str = "ru-moscow-1"
    sfs_default_size: str = 30
    sfs_vpc_id: str = None


settings = Settings()
