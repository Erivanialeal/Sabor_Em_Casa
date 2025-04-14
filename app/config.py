#configuracoes do banco de dados
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class Config:
    # config.py
    SECRET_KEY = os.getenv('SECRET_KEY')  # Segurança
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa notificações desnecessárias do SQLAlchemy
    JWT_SECRET_KEY = "super-secret"  # Change this!
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization' # Nome do cabeçalho HTTP para o token JWT
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30) #define o tempo de vida do token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=86400)
    JWT_ALGORITHM = 'HS256'


