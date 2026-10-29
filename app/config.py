from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Financial Risk Analysis API"
    database_url: str = "sqlite:///./data/risk_analysis.db"
    api_key: str = ""
    high_amount_threshold: float = 50000.0
    frequency_count_threshold: int = 5
    frequency_window_minutes: int = 10
    high_amount_risk: int = 40
    frequency_risk: int = 35
    region_change_risk: int = 25
    alert_score_threshold: int = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
