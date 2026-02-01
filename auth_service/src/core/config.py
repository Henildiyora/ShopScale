from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application Configuration Management.
    
    Loads environment variables from .env file and verifies types.
    """

    PROJECT_NAME : str = "ShopScale Auth Service"
    DATABASE_URL : str = "postgresql+asyncpg://admin:password@localhost:5432/auth_db"
    SECERET_KEY : str = "super_secret_key_for_dev_only"
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : str = 30

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

 