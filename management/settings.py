from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    DB_NAME: str = "dbname"
    DB_USER: str = "dbuser"
    DB_PASS: str = "pass"

    class Config:
        env_file = ".env"


class DevAppSettings(BaseAppSettings):
    DB_NAME: str = "dbname"
    DB_USER: str = "dbuser"
    DB_PASS: str = "pass"

    class Config:
        env_file = ".env"


class TestAppSettings(BaseAppSettings):
    DB_NAME: str = "dbname"
    DB_USER: str = "dbuser"
    DB_PASS: str = "pass"

    class Config:
        env_file = ".env"
