#arquivo principal
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy #para conectar,criar,Mapeamento Objeto-Relacional (ORM)
#O ORM (Object-Relational Mapping) do SQLAlchem e gerenciar o banco de dados
from flask_migrate import Migrate 
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)  # Adiciona esta linha para inicializar o Flask-Migrate

# Importa os modelos (depois de inicializar o db)
from models import *

if __name__ == '__main__':
    app.run(debug=True)
