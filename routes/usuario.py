from flask import Blueprint, request, jsonify
from app.extensions import db  # Certifique-se de que `db` está configurado corretamente
from app.models import Usuario,Enderecos
from werkzeug.security import generate_password_hash,check_password_hash
from app.extensions import create_access_token,jwt_required,get_jwt_identity,datetime,timedelta,decode_token
from app.extensions import configuracao


# Criação do Blueprint para usuários
usuario_bp = Blueprint('usuario', __name__)

# Rota de boas vindas
@usuario_bp.route('/', methods=['GET'])
def index():
    return jsonify({"mensagem": "Bem-vindo"})

# Rota para cadastrar o usuário
@usuario_bp.route('/listar_usuarios', methods=['GET']) # Rota para listar usuários
def listar_usuarios():
    # Verifica se o usuário é um administrador
    usuarios=Usuario.query.all() #Recupera todos os usuários do banco de dados
    if not usuarios:
        return jsonify({"mensagem":"Nenhum usuário encontrado"}), 404 #Retorno quando um recurso não é encontrado.
    # Criar uma lista de contatos
    usuarios_lista = [usuarios.to_dict() for usuarios in usuarios] # Cria uma lista de dicionarios com os dados dos [usuários]
        # Retornar os dados no formato JSON
    return jsonify(usuarios_lista), 200 # Retorno quando uma página ou recurso é carregado corretamente.
    
@usuario_bp.route('/detalhes_usuario/<id>', methods=['GET']) # Rota para detalhes do usuário
def detalhes_usuario(id):
    usuario = Usuario.query.get(id) # Busca o usuário pelo ID
    if not usuario:
        return jsonify({"mensagem":"Usuário não encontrado"}), 404
    # Retorna os detalhes do usuário
    return jsonify(usuario.to_dict()),200 

# Criar um novo usuário
@usuario_bp.route('/cadastrar', methods=['POST']) # Rota para cadastrar um novo usuário
def criar_usuario():
    dados = request.get_json() # Obter os dados da requisição
    if not dados:
        return jsonify({"erro":"Nenhum dado json enviado"}),400 # Retorno quando não há dados JSON enviados na requisição.
    nome= dados.get('nome')
    email= dados.get('email')
    telefone= dados.get('telefone')
    senha_hash= dados.get('senha_hash')
    tipo_de_usuario= dados.get('tipo_de_usuario')
    # Verifica se todos os campos obrigatórios estão presentes
    campos_obrigatorios = ['nome', 'email', 'telefone', 'senha_hash', 'tipo_de_usuario']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({'erro':f"Campo obrigatorio {campo} não foi encontrado"}),400 # Retorno quando um campo obrigatório não é encontrado.
        # Verifica se email já está em uso
    usuario_existente=Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({"erro":"Email já cadastrado"}),400
    # Cria o novo usuário
    senha_hash=generate_password_hash(senha_hash) # Gera o hash da senha
    # Cria o novo usuário com os dados fornecidos
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        telefone=telefone,
        senha_hash=senha_hash,
        tipo_de_usuario=tipo_de_usuario # Define o tipo de usuário

    )
    try:
        # adicionar um novo usário ao banco de dados
        db.session.add(novo_usuario) # Adiciona o novo usuário à sessão do banco de dados
        db.session.commit() # Salva as alterações no banco de dados
        return jsonify({"mensagem":"Usuário cadastrado com sucesso!"}), 201 # Retorno quando um novo recurso é criado com sucesso.
    except Exception as e:
        db.session.rollback() # Reverte alterações em caso de erro

# Adualizar dados de um usuário
@usuario_bp.route('/atualizar_usuario/<int:id>', methods=['PUT']) # Rota para atualizar um usuário
def atualizar_usuario(id):
    usuario=Usuario.query.get(id) # Buscar o usuario pelo ID
    if not usuario:
        return jsonify({"erro":"Nenhum usuário encontrado"}), 404 # Retorno quando um recurso não é encontrado.
    dados=request.get_json() #Obter os dados da requisição
    if not dados:
        return jsonify({"erro": "Nenhum dado json enviado"}), 400 
    usuario.nome=dados.get('nome',usuario.nome) # Atualiza o nome do usuário
    usuario.email=dados.get('emai', usuario.email)
    usuario.telefone=dados.get('telefone', usuario.telefone)
    usuario.senhas_hash=dados.get('senha_hash', usuario.senha_hash)
    usuario.tipo_de_usuario=dados.get('tipo_de_usuario', usuario.tipo_de_usuario)
    # salvar as alterações
    db.session.commit()
    return jsonify({"mensagem":"Usuário atualizado com sucesso"})


@usuario_bp.route('/deletar_usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario=Usuario.query.get(id) #Buscar o usuario pelo ID
    print(usuario)
    if not usuario:
        return jsonify({'mensagem':'Nenhum usuário encontrado!'}), 404 # Rteorno quando um usuário não é encontrado.
    try:
    
        db.session.delete(usuario) # Deletar o usuário
        db.session.commit() #salvar as alterações feita
        return jsonify({"mensagem":" Usuário deletado com sucesso!"}), 200 # Retorno quando um recurso é deletado com sucesso.
    except Exception as e : # casso ocorrer um erro
        db.session.rollback() # Reverter alterações em caso de erro
        return jsonify({"erro":"Erro ao deletar usuário"}), 500 # Retorno quando ocorre um erro interno do servidor.
    
@usuario_bp.route('/autenticar_usuario/login', methods=['POST'])
def autenticar_usuario():
    dados= request.get_json() # Obter os dados da requisição
    print(dados)
    if not dados:
        return jsonify({'mensagem':'Nenhum dado Json enviado'}), 404 #retorno quando um recurso não é encontrado
    nome= dados.get('nome')
    print(nome)
    senha= dados.get('senha')
    print(senha)
    if not nome or not senha: # Verifica se o usário e a senha foram informados
        return jsonify({'mensagem':'Usuário ou senha não informados'}), 404 # Retorno quando um recurso não é encontrado.
    # Verificar se o usuário existe
    usuario_obj=Usuario.query.filter_by(nome=nome).first()
    if not usuario_obj:
        return jsonify({"mensagem":"Usuário não encontrado"}), 404 # Retorno quando um recurso não é encontrado.
    # Verificar se a senha está correta
    if not check_password_hash(usuario_obj.senha_hash, senha): # Verifica se a senha está correta
        print(f"Senha digitada: {senha}") 
        print(f"Senha no banco (hash): {usuario_obj.senha_hash}")
        return jsonify({"mensagem":"Senha incorreta"}), 401 # Retorno quando a autenticação falha.
    # Gerar o token JWT
    token = create_access_token(identity=nome.id, expires_delta=timedelta(days=1))
    # Retornar o token JWT
    return jsonify({"token":token}), 200 # Retorno quando uma página ou recurso é carregado corretamente.



    


    

