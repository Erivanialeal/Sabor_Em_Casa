#configuracoes do banco de dados
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # config.py
    SECRET_KEY = os.getenv('SECRET_KEY')  # Segurança
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa notificações desnecessárias do SQLAlchemy



