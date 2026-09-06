import os


class Settings:
    """
    Centraliza as configurações da aplicação, lidas de variáveis de ambiente.
    Em produção (docker-compose) essas variáveis virão do .env.
    Em testes, usamos valores padrão que apontam para SQLite/fakeredis.
    """

    # Banco de dados
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db",  # fallback simples para rodar local sem Postgres
    )

    # Redis (cache)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Se True, usamos fakeredis em vez de um Redis real (usado nos testes)
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"

    # Tamanho do código curto gerado (ex: abc123)
    SHORT_CODE_LENGTH: int = int(os.getenv("SHORT_CODE_LENGTH", "6"))

    # Tempo de vida do cache no Redis, em segundos
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))


settings = Settings()
