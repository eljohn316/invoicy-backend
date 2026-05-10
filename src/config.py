from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    secret_key: SecretStr
    algorithm: str = "HS256"
    # 60 minutes * 24 hours * 7 days = 7 days
    access_token_expire_minutes: int = 60 * 24 * 7
    environment: Literal["local", "staging", "production"] = "local"
    cors_origins: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.cors_origins]


settings = Settings()
