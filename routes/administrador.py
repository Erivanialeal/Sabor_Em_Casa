from flask import jsonify,Blueprint,request
from functools import wraps
from app.extensions import jwt_required,get_jwt_identity
#Middleware para verificar se usuario é administrador
def admin_requirend(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        indentity= get_jwt_identity()
        if indentity != 'administrador':
            return jsonify({"message": "Acesso negado"}),403
        return fn(*args, **kwargs)
    return wrapper

#rota painel administrador
administrador_bp = Blueprint('administrador', __name__)

@administrador_bp.route('/',methods=['GET'])
@admin_requirend
def administrador():
    return jsonify({'message': "Bem Vindo! Ao painel do administrador!"})

