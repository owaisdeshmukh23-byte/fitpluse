import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration for PulseFit."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'pulsefit-super-secret-key-college-project-2026')
    
    # Render and Heroku provide DATABASE_URL starting with postgres://
    # SQLAlchemy 2.0+ requires postgresql://
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Default local PostgreSQL connection configuration
        db_user = os.environ.get('POSTGRES_USER', 'postgres')
        db_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
        db_host = os.environ.get('POSTGRES_HOST', 'localhost')
        db_port = os.environ.get('POSTGRES_PORT', '5432')
        db_name = os.environ.get('POSTGRES_DB', 'pulsefit_db')
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    elif database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {
            "connect_timeout": 3
        }
    }
