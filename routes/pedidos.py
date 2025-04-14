from flask import Blueprint,request,jsonify
from app.extensions import jwt_required,get_jwt_identity
from app.models import Pedidos

pedido_bp = Blueprint('pedido',__name__)
@pedido_bp.route("/listar_pedidos",methods=['GET'])
def listar_pedidos():
    pedidos=Pedidos.query.all()
    if not pedidos:
        return jsonify({"erro":"Nenhum pedido encontrado"}),404
    lista = []
    for pedido in pedidos:
        lista.append({
            "usuario":pedido.usuario,
            "total":pedido.total,
            "status":pedido.status,
            "criado_em":pedido.criado_em
        })
    return jsonify(lista),200

@pedido_bp.route("/detalhes_pedido/<int:id>",methods=["GET"])
def detalhes_do_pedido(id):
    if id <= 0:
        return jsonify({"erro":"ID invalido"}),404
    #buscar o pedido no banco
    pedidos=Pedidos.query.get(id)
    if not pedidos:
        return jsonify({"erro":"Nehum produtos encontrado"}),404
    #ver se os bancos dos pedidos são válidos
    informacoes_pedidos={
        'id':pedidos.id,
        'usuario':pedidos.usuario,
        'status':pedidos.status,
        'total':pedidos.total,
        'criado_em':pedidos.criado_em
    }
    return jsonify(informacoes_pedidos),200
    
    