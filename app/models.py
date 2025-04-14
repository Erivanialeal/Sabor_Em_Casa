#modelo do banco de dados
from app.extensions import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash




#db.Model é a classe base do SQLAlchemy para mapear a tabela do 
# banco de dados a uma classe Python (ORM - Object Relational Mapping).
class Usuario(db.Model):
    __tablename__='usuarios' #nome da tabela

    id=db.Column(db.Integer,primary_key=True)
    nome=db.Column(db.String(50),nullable=False,unique=True)#nullable=false torna obrigatorio o preenchimento dessa coluna
    email=db.Column(db.String(120),nullable=False,unique=True)#unique=true Garante que os valores nesta coluna sejam únicos
    telefone=db.Column(db.String(20), nullable=False)
    tipo_de_usuario= db.Column(db.Enum("comum","Administrador",name='tipo_usuario_enum'),nullable=False, default="comum")
    senha_hash = db.Column(db.String(512), nullable=False) 
    
    def __init__(self, nome, email, telefone,tipo_de_usuario ,senha_hash):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.Tipo_de_usuario=tipo_de_usuario
        self.senha_hash =senha_hash

    def set_tipo_de_usuario(self,novo_tipo,authorized=False):
        if novo_tipo =='administrador' and not authorized:
            raise ValueError("Somente usuários autorizados podem ser definidos como administradores.")
        self.tipo_de_usuario = novo_tipo
    

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# Definição da classe Produtos
class Produtos(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome_produto}>'

# Definição da classe Estoque
class Estoque(db.Model):
    __tablename__ = 'estoque'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # Relação com a tabela Produtos
    produto = db.relationship('Produtos', backref='estoque', lazy=True)

    def __repr__(self):
        return f"<Estoque(id={self.id})>"

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
    usuario_id=db.Column(db.Integer,db.ForeignKey('usuarios.id'),nullable=False)
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
    usuario_id=db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)
    data_pagamento=db.Column(db.DateTime,nullable=False)
    metodo_pagamento=db.Column(db.String(50),nullable=False)
    valor_pagamento=db.Column(db.Numeric(10,2), nullable=False)
    status_pagamento=db.Column(db.String(20),nullable=False)
    data_confirmacao=db.Column(db.DateTime,nullable=True)
    detalhes_pagamento=db.Column(db.Text,nullable=True)

    def __repr__(self):
        return f'< Pagamento {self.id}>'
    
class Enderecos(db.Model):
    __tablename__='enderecos'

    id=db.Column(db.Integer, primary_key=True)
    usuario_id=db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)
    rua=db.Column(db.String(100),nullable=False)
    numero=db.Column(db.String(50), nullable=False)
    complemento=db.Column(db.String(100), nullable=False)
    bairro=db.Column(db.String(100),nullable=False)
    cidade=db.Column(db.String(100),nullable=False)
    estado=db.Column(db.String(100),nullable=False)
    cep=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f'<Endereço id={self.rua}>'
    
