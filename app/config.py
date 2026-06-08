from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", protected_namespaces=())

    model_id: str = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    max_new_tokens: int = 200
    max_upload_bytes: int = 10485760
    hf_token: str


settings = Settings()
