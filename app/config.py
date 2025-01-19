import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Configuration class for Flask app. Dynamically selects the database URL
    based on the TEST environment variable.
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    TEST = os.getenv("TEST", "false").lower() == "true"

    # Production and Test database URLs
    DB_URL = os.getenv("DB_URL")
    TEST_DB_URL = os.getenv("TEST_DB_URL")

    # Determine the database URL based on TEST
    SQLALCHEMY_DATABASE_URI = DB_URL if not TEST else TEST_DB_URL

    @staticmethod
    def validate():
        """
        Validate the configuration to ensure required variables are set.
        """
        if not Config.SQLALCHEMY_DATABASE_URI:
            raise RuntimeError(
                "Database URL is missing. Check your .env file."
            )


class TestConfig(Config):
    """
    Test configuration class.
    Overrides the database URI to use an in-memory SQLite database.
    """

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True  # Enable testing mode
