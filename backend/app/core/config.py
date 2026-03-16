"""Application settings loaded from environment variables."""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Central configuration using Pydantic BaseSettings."""

    # LLM Provider
    llm_provider: str = Field(default="groq", description="LLM provider: 'groq' or 'openai'")
    groq_api_key: str = Field(default="", description="Groq API key")
    openai_api_key: str = Field(default="", description="OpenAI API key")
    groq_model: str = Field(default="llama-3.1-8b-instant", description="Groq model name")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI model name")

    # File Storage
    upload_dir: str = Field(default="./uploads", description="Directory for uploaded files")
    chart_dir: str = Field(default="./charts", description="Directory for generated charts")

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")

    # CORS
    frontend_url: str = Field(default="http://localhost:5173", description="Frontend URL for CORS")

    # File Limits
    max_file_size_mb: int = Field(default=50, description="Maximum upload file size in MB")
    allowed_extensions: list[str] = Field(
        default=[".csv", ".xlsx", ".xls"],
        description="Allowed file extensions",
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    def ensure_directories(self) -> None:
        """Create upload and chart directories if they don't exist."""
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
        Path(self.chart_dir).mkdir(parents=True, exist_ok=True)


# Singleton settings instance
settings = Settings()
