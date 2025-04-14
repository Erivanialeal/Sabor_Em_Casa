from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,decode_token
from datetime import datetime,timedelta
from jwt import PyJWK
from app.config import Config

# Inicialize as extensões sem vinculá-las ao app ainda
db = SQLAlchemy()
migrate = Migrate()
jwt= JWTManager()
data= datetime.now()
configuracao=Config()
