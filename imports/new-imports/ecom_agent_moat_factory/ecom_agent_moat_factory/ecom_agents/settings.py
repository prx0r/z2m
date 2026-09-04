from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    admin_token: str = os.getenv("ADMIN_TOKEN", "dev-token")
    database_path: str = os.getenv("DATABASE_PATH", "./ecom_agents.db")
    shopify_store_domain: str = os.getenv("SHOPIFY_STORE_DOMAIN", "")
    shopify_admin_token: str = os.getenv("SHOPIFY_ADMIN_TOKEN", "")
    retell_api_key: str = os.getenv("RETELL_API_KEY", "")
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    inworld_api_key: str = os.getenv("INWORLD_API_KEY", "")
    aftership_api_key: str = os.getenv("AFTERSHIP_API_KEY", "")
    aftership_webhook_secret: str = os.getenv("AFTERSHIP_WEBHOOK_SECRET", "")
    gorgias_domain: str = os.getenv("GORGIAS_DOMAIN", "")
    gorgias_email: str = os.getenv("GORGIAS_EMAIL", "")
    gorgias_api_key: str = os.getenv("GORGIAS_API_KEY", "")

settings = Settings()
