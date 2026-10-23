from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str
    mail_port: int = 587
    mail_starttls: bool = True
    mail_ssl_tls: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def mail_config(self) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self.mail_username,
            MAIL_PASSWORD=self.mail_password,
            MAIL_FROM=self.mail_from,
            MAIL_SERVER=self.mail_server,
            MAIL_PORT=self.mail_port,
            MAIL_STARTTLS=self.mail_starttls,
            MAIL_SSL_TLS=self.mail_ssl_tls,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

settings = Settings()
