from flask import Flask
from app.config import Config 
from app.extensions import db, migrate # Exemplo, ajuste conforme necessário
from flask_jwt_extended import JWTManager
from routes import register_blueprints

# Função para criar a aplicação
def criar():
    app = Flask(__name__)
    app.config.from_object(Config) #carrega as configurações da minha aplicação

    db.init_app(app) #inicializa o objeto do banco de dados(db)
    migrate.init_app(app,db)#inicializa o gerenciador de migrações(migrate)
    jwt=JWTManager(app)

    # Registre as rotas e blueprints
    register_blueprints(app)#registra o blueprints na aplicação flask

    return app

# Para rodar a aplicação
if __name__ == '__main__':
    app = criar()
    app.run(debug=True)
