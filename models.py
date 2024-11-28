#modelo do banco de dados
from app import db

#db.Model é a classe base do SQLAlchemy para mapear a tabela do 
# banco de dados a uma classe Python (ORM - Object Relational Mapping).
class User(db.Model):
    __tablename__='users' #nome da tabela
    __table_args__ = {'extend_existing': True}#Um dicionário que contém argumentos adicionais para a tabela.


    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome_usuario=db.Column(db.String(50),nullable=False,unique=True)#nullable=false torna obrigatorio o preenchimento dessa coluna
    email=db.Column(db.String(120),nullable=False,unique=True)#unique=true Garante que os valores nesta coluna sejam únicos
    role=db.Column(db.String(20))
    senha_hash =db.Column(db.String(128),nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'
    
class Produtos(db.Model):
    __tablename__='produtos'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome_produto=db.Column(db.String(50),nullable=False)
    preco=db.Column(db.Numeric(10,2),nullable=False)
    descricao=db.Column(db.Text)
    categoria=db.Column(db.Integer,db.ForeignKey('categorias.id'),nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome_produto}>'
    
class Categoria(db.Model):
    __tablename__='categorias'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome_categoria=db.Column(db.String(50),nullable=False,unique=True)

    def __repr__(self):
        return f'<Categoria {self.nome_categoria}>'
    
class Pedidos(db.Model):
    __tablename__='pedidos'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    usuario_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    total=db.Column(db.Numeric(10,2), nullable=False)
    status=db.Column(db.String(20), nullable=False)
    criado_em = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Pedido {self.id}>'

class ItemPedido(db.Model):
    __tablename__='itens_pedido'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    pedido_id=db.Column(db.Integer, db.ForeignKey('pedidos.id'),nullable=False)
    produtos_id=db.Column(db.Integer, db.ForeignKey('produtos.id'),nullable=False)
    quantidade=db.Column(db.Integer, nullable=False)
    preco=db.Column(db.Numeric(10,2), nullable=False)

    def __repr__(self): 
        return f'<ItemPedido {self.id}>'
    
class Pagamento(db.Model):
    __tablename__='pagamentos'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    pedido_id=db.Column(db.Integer, db.ForeignKey('pedidos.id'),nullable=False)
    usuario_id=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    data_pagamento=db.Column(db.DateTime,nullable=False)
    metodo_pagamento=db.Column(db.String(50),nullable=False)
    valor_pagamento=db.Column(db.Numeric(10,2), nullable=False)
    status_pagamento=db.Column(db.String(20),nullable=False)
    data_confirmacao=db.Column(db.DateTime,nullable=True)
    detalhes_pagamento=db.Column(db.Text,nullable=True)

    def __repr__(self):
        return f'< Pagamento {self.id}>'
    
class Ederecos(db.Model):
    __tablename__='endereços'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    usuario_id=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    rua=db.Column(db.String(100),nullable=False)
    numero=db.Column(db.String(50), nullable=False)
    complemento=db.Column(db.String(100), nullable=False)
    bairro=db.Column(db.String(100),nullable=False)
    cidade=db.Column(db.String(100),nullable=False)
    estado=db.Column(db.String(100),nullable=False)
    cep=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f'<Endereço id={self.id} usuario_id{self.usuario_id}>'
    
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Estoque(db.Model):
    __tablename__ = 'estoque'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # Relação com a tabela Produtos (se existir)
    produto = db.relationship('Produto', backref='estoque', lazy=True)

    def __repr__(self):
        return f"<Estoque(id={self.id}, produto_id={self.produto_id}, quantidade={self.quantidade}, atualizado_em={self.atualizado_em})>"



