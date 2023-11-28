from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    # DB_NAME: str = "dbname"
    # DB_USER: str = "dbuser"
    # DB_PASS: str = "pass"
    # DB_HOST: str = "database"
    # DB_PORT: int = 5432
    #
    # class Config:
    #     env_file = ".env"
    pass


class DevAppSettings(BaseAppSettings):
    # DB_NAME: str = "dbname"
    # DB_USER: str = "dbuser"
    # DB_PASS: str = "pass"
    # DB_HOST: str = "database"
    # DB_PORT: int = 5432
    #
    # class Config:
    #     env_file = ".env"
    pass


class TestAppSettings(BaseAppSettings):
    # DB_NAME: str = "dbname"
    # DB_USER: str = "dbuser"
    # DB_PASS: str = "pass"
    # DB_HOST: str = "database"
    # DB_PORT: int = 5432
    #
    # class Config:
    #     env_file = ".env"
    pass
