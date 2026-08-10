from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM :
    OPENAI_API_KEY :str
    LANGCHAIN_TRACING_V2 : bool = False
    LANGCHAIN_API_KEY :str = ""
    LANGCHAIN_PROJECT : str = "genesis-ai"

    # Weather
    WEATHER_API_KEY : str = ""

    # Storage
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    DATABASE_URL: str = "sqlite:///./data/genesis.db"

    ENVIRONMENT: str = "dev"
    LOG_LEVEL: str = "INFO"

settings = Settings()

#________ # _________ # 

"""Basically in this file we are defining the configuration settings for the application using Pydantic's BaseSettings.
   In simple terms, this file contains all the configuration variables that can be set as environment variables or in a .env file. and also an skeleton structure """
# This file acts as the central hub for all the configuration variables your application needs to run properly.
#  Instead of hardcoding secrets or settings throughout your code, you keep them in one place.
#  It manages things like API keys, database URLs, file paths, and your environment mode.