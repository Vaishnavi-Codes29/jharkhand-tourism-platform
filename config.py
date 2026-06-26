"""
Configuration file for Jharkhand Tourism Application
Centralized settings for easy management and customization
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    
    # Database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "database.db"))
    
    # API Keys
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    
    # Server
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = FLASK_ENV == "development"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")  # Must be set in production

# Select config based on environment
config = DevelopmentConfig if os.environ.get("FLASK_ENV") == "development" else ProductionConfig
