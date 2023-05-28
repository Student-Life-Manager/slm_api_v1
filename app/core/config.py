from pydantic import BaseSettings, PostgresDsn, RedisDsn


class SLMBaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class AuthConfig(SLMBaseConfig):
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_TIME_IN_DAYS: int = 1
    JWT_ACCESS_TOKEN_EXPIRY_IN_DAYS: int = 1
    JWT_REFRESH_TOKEN_EXPIRY_IN_DAYS: int = 5


class SentryConfig(SLMBaseConfig):
    SENTRY_DSN: str = ""
    SENTRY_ENVIRONMENT: str = ""


class AWSConfig(SLMBaseConfig):
    EMAIL_DOMAIN: str = ""
    AWS_REGION: str = ""


class TwilioConfig(SLMBaseConfig):
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_SENDER_PHONE_NUMBER: str = ""


class Settings(SLMBaseConfig):
    SENTRY_CONFIG: SentryConfig = SentryConfig()
    TWILIO_CONFIG: TwilioConfig = TwilioConfig()
    AUTH_CONFIG: AuthConfig = AuthConfig()

    DEBUG: int = 0
    ENVIRONMENT: str = "development"
    POSTGRES_URL: PostgresDsn = "postgresql://slm_user:slm@127.0.0.1:5432/slm-db"
    DATABASE_URL: PostgresDsn = "postgresql://slm_user:slm@127.0.0.1:5432/slm-db"
    RELEASE_VERSION: str = "dev"
    SHOW_SQL_ALCHEMY_QUERIES: int = 1
    SHOW_OUTGOING_REQUESTS: int = 1
    ALLOWED_EMAIL_DOMAIN: str = "srmap.edu.in"


settings = Settings()