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

    def to_dict(self):
        return {
            'id':self.id,
            'nome':self.nome,
            'email':self.email,
            'telefone':self.telefone,
            'tipo_de_usuario':self.tipo_de_usuario,
        }
    

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# Definição da classe Produtos
class Produtos(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True) # ID do produto
    nome = db.Column(db.String(50), nullable=False) # Nome do produto
    descricao = db.Column(db.Text) # Descrição do produto
    imagem=db.Column(db.String(100)) # URL ou caminho da imagem do produto
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False) # Chave estrangeira para a tabela categorias

    def __repr__(self):
        return f'<Produto {self.nome}>' # Nome do produto

class TamanhosProdutos(db.Model): # Definição da tabela de tamanhos dos produtos.
    __tablename__="tamanhos_produtos"
    
    id= db.Column(db.Integer,primary_key=True,autoincrement=True) # ID do tamanho 
    nome=db.Column(db.String(50),nullable=False,unique=True) # Nome do tamanho

class PrecosProdutos(db.Model): # Definição da tabela de preços dos produtos.
    __tablename__="precos_produtos"
    id= db.Column(db.Integer, primary_key=True,autoincrement=True) # ID do preço
    produto_id= db.Column(db.Integer,db.ForeignKey('produtos.id'),nullable=False) # Chave estrageira para a tabela produtos
    tamanho_id=db.Column(db.Integer,db.ForeignKey('tamanhos_produtos.id'),nullable=False) # Chave estrangeira para a tabela tamanhos_produtos
    preco=db.Column(db.Numeric(10,2),nullable=False) # Preço do produto

class Ingredientes(db.Model): # Definição da tabela de ingredientes dos produtos.
    __tablename__="ingredientes"
    id= db.Column(db.Integer,primary_key =True, autoincrement=True)
    nome= db.Column(db.String(50),nullable=False,unique=True) # Nome do ingrediente
    quantidade_em_estoque= db.Column(db.Integer,nullable=False) # Qunatidade do ingrediente em estoque

# Definição da classe Estoque
class Estoque(db.Model):
    __tablename__ = 'estoque'

    id = db.Column(db.Integer, primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False) # Chave estrageira para a tabela ingredientes
    quantidade_disponivel = db.Column(db.Integer, nullable=False) # Quantidade disponível do ingrediente

class Categoria(db.Model):
    __tablename__='categorias'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome=db.Column(db.String(50),nullable=False,unique=True)
    descricao=db.Column(db.Text,nullable=False)
    imagem=db.Column(db.String(100),nullable=False) # URL ou caminho da imagem da categoria

    def __repr__(self):
        return f'<Categoria {self.nome}>'
    
class Pedidos(db.Model):
    __tablename__='pedidos'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    usuario_id=db.Column(db.Integer,db.ForeignKey('usuarios.id'),nullable=False)
    data_do_pedido=db.Column(db.DateTime,nullable=False)
    status_id=db.Column(db.Integer, db.ForeignKey('status_pedido.id'),nullable=False) # chave estrageira para a tabela status_pedido
    endereco_id=db.Column(db.Integer, db.ForeignKey('enderecos.id'),nullable=False)
    pagamento_id=db.Column(db.Integer, db.ForeignKey('pagamentos.id'),nullable=False) # chave estrageira para a tabela pagamentos
    valor_total=db.Column(db.Numeric(10,2),nullable=False)
    criado_em = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Pedido {self.id}>'

class ItemPedido(db.Model):
    __tablename__='itens_pedido' 
    __table_args__={'extend_existing':True} 

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    pedido_id=db.Column(db.Integer, db.ForeignKey('pedidos.id'),nullable=False) # chave estrageira para a tabela pedidos
    produto_id=db.Column(db.Integer, db.ForeignKey('produtos.id'),nullable=False) # chave estrageira para a tabela produtos
    quantidade=db.Column(db.Integer, nullable=False) 
    preco_unitario=db.Column(db.Numeric(10,2), nullable=False)
    sub_total=db.Column(db.Numeric(10,2),nullable=False) # Valor total do item (quantidade)

    def __repr__(self): 
        return f'<ItemPedido {self.id}>' 
    
class Pagamento(db.Model):
    __tablename__='pagamentos'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome=db.Column(db.String(50),nullable=False) # Nome do método de pagamento
    descricao=db.Column(db.Text,nullable=False) # Descrição do método de pagamentos

    def __repr__(self):
        return f'< Pagamento {self.id}>'
    
class StatusPedido(db.Model):
    __tablename__='status_pedido'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome=db.Column(db.String(50),nullable=False) # Nome do status do pedido
    descricao=db.Column(db.Text,nullable=False) # Descrição do status do pedido

    def __repr__(self):
        return f'<StatusPedido {self.nome}>'
    
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

    def to_dict(self):
        return{
            'id':self.id,
            'usuario_id':self.usuario_id,
            'rua':self.rua,
            'numero':self.numero,
            'complemento':self.complemento,
            'bairro':self.bairro,
            'cidade':self.cidade,
            'estado':self.estado,
            'cep':self.cep
        }


    def __repr__(self):
        return f'<Endereço id={self.rua}>'
    
