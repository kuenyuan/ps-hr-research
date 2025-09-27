import os from pydantic import
   BaseSettings

   class Settings(BaseSettings):  groq_api_key: str | None =
   os.getenv("GROQ_API_KEY")  google_client_id: str | None =
   os.getenv("GOOGLE_CLIENT_ID")  google_client_secret: str | None =
   os.getenv("GOOGLE_CLIENT_SECRET")  blogger_client_id: str | None =
   os.getenv("BLOGGER_CLIENT_ID")  blogger_client_secret: str | None =
   os.getenv("BLOGGER_CLIENT_SECRET")  blogger_redirect_uri: str | None =
   os.getenv("BLOGGER_REDIRECT_URI")  wordpress_base_url: str | None =
   os.getenv("WORDPRESS_BASE_URL")  wordpress_username: str | None =
   os.getenv("WORDPRESS_USERNAME")  wordpress_app_password: str | None =
   os.getenv("WORDPRESS_APP_PASSWORD")  unpaywall_email: str | None =
   os.getenv("UNPAYWALL_EMAIL")  semantic_scholar_api_key: str | None =
   os.getenv("SEMANTIC_SCHOLAR_API_KEY")  sqlite_url: str = os.getenv("SQLITE_URL",
   "sqlite:///data/app.db")  environment: str = os.getenv("ENV", "dev")

   settings = Settings()