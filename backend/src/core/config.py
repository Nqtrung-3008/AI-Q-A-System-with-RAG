from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    
    OLLAMA_BASE_URL: str
    OLLAMA_LLM_MODEL: str

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    EMBED_MODEL: str
    TOP_K: int

    model_config = SettingsConfigDict(
        env_file=".env"
    )
        
settings = Settings()