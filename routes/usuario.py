from flask import Blueprint, request, jsonify
from extensions import db  # Certifique-se de que `db` está configurado corretamente
from models import Usuario,Enderecos
from werkzeug.security import generate_password_hash,check_password_hash
from extensions import create_access_token,jwt_required,get_jwt_identity,datetime,timedelta,decode_token
from extensions import configuracao


# Criação do Blueprint para usuários
usuario_bp = Blueprint('usuario', __name__)

# Rota de boas vindas
@usuario_bp.route('/', methods=['GET'])
def index():
    return jsonify({"mensagem": "Bem-vindo"})

# Rota para cadastrar o usuário
@usuario_bp.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    # Pega os dados enviados no corpo da requisição
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    role = data.get('role','comun')
    senha = data.get('senha')

    # Verifica se todos os dados obrigatórios foram enviados
    if not nome or not email or not role or not senha:
        return jsonify({"message": "Todos os campos são obrigatórios!"}), 400
    
    #Verifica se o email já existe no banco de dados
    usuario_existente=Usuario.query.filter_by(email=email).first()#verifica se existe um usuário no banco de dados
    if usuario_existente:
        return jsonify({"mensage":"Este email já está cadastrado!"}),400 #Indica que a requisição não pôde ser entendida pelo servidor devido a uma sintaxe inválida.

    # Criptografa a senha
    senha_hash = generate_password_hash(senha, method='scrypt', salt_length=16)
    print("Hash gerado no cadastro:", senha_hash)

    # Cria o novo usuário

    novo_usuario = Usuario(nome=nome, email=email, role=role, senha_hash=senha_hash)

    try:
        # Adiciona o usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201 #Indica que a requisição foi bem-sucedida e um novo recurso foi criado.

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro interno ao cadastrar usuario"}), 500 #Retornado quando há um erro no servidor, como um problema no código ou uma falha no banco de dados.

#rota de login
@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    print(f"Email recebido: {email}")
    print(f"Senha recebida: {senha}")

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        print("Usuário não encontrado no banco de dados.")
        return jsonify({"message": "Usuário não encontrado."}), 401
    
    print(f"Senha enviada: {senha}")
    print(f"Senha armazenada (hash): {usuario.senha_hash}")

    if not check_password_hash(usuario.senha_hash, senha):
        return jsonify({"message": "Senha inválida."}), 401 #Retornado quando um usuário tenta acessar um recurso protegido sem fornecer credenciais válidas.
    
    
    # Cria um token de acesso
    acesso_token = create_access_token(identity=str(usuario.role))
    return jsonify(acesso_token=acesso_token), 200 #Retornado quando uma página ou recurso é carregado corretamente.

@usuario_bp.route('/renovar_token',methods=['POST'])
@jwt_required(refresh=True)

#TESTAR ESSA ROTA COM MAIS DETALHES
def refresh_token():
    #obter o indentificador  do úsuario do token de refresh
    usuario_atual= get_jwt_identity()
    #criar um novo tokem de acesso.
    novo_token_de_acesso= create_access_token(indenty=usuario_atual)

    return jsonify(access_token=novo_token_de_acesso),200

#TESTAR ESSA ROTA COM MAIS DETALHES
BLACKLIST = set() # serve para invalidar tokens que não devem mais ser usados.           
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    cabeçalho= request.headers.get('Authorization')
    if not cabeçalho or not cabeçalho.startswith('Bearer'): #startswith é usado para verificar se um string começã com um prefixo especifico.
        return jsonify({"mensagem":"Token inválido ou ausente,"}),400
    token=cabeçalho.split("")[1] #extrai o token do header
    BLACKLIST.add(token) #adiciona o token na blacklist

    return jsonify({'mensagem':"Logout realizado com sucesso"}), 200

@usuario_bp.route('/recuperar_senha',methods=['POST'])
def recuperar_senha():
    dado= request.get_json() #obter os dados
    email= dado.get('email')
    if not email:
        return jsonify({'message': 'E-mail e obrigatório'}),400
    
    #verifica se o email existe no banco de dados
    user=Usuario.query.filter_by(email=email).first() #busca usuario pelo email
    if not user:
        return jsonify({'message':'Voçê receberar instruções de recuperação.'}),200

    #gerar o toke
    token = create_access_token(identity=str(user.id))

     # Retornar o token diretamente (para teste no Insomnia)
    return jsonify({'message': 'Token gerado com sucesso.', 'token': token}), 200

@usuario_bp.route('/redefinir_senha', methods=['POST'])
def redefinir_senha():
    dado=request.get_json()#obter dados

    #ver se os dados foram fornecidos
    if not dado:
        return jsonify({"message":"Erro dados não fornecidos."}),400
    
    token= dado.get('token')
    nova_senha=dado.get('nova_senha')

    if not token or not nova_senha:
        return jsonify({'erro': 'Token e nova senha são obrigatórios'}),400
    try:
    #decodificar o token
        decoded=decode_token(token)
        user_id=decoded.get('sub')#id do usuario no token

        if not  user_id:
            return jsonify({'Message':' Token inválido ou expirado'}),400

    except Exception as e:
        print(f"Erro ao decodificar o token: {str(e)}")
        return jsonify({'message': 'Token inválido ou expirado'}), 400
    
    #valida a nova senha
    if len(nova_senha)< 8:
        return jsonify({'Message':'Senha deve ter pelo menos 8 caracters'}),400
    
    hashed_password= generate_password_hash(nova_senha)
    print(f"Senha atualizada para o usuário {user_id}:{hashed_password}")

    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), 404

    user.senha = hashed_password
    db.session.commit()

    print(f"Senha atualizada com sucesso para o usuário {user_id}.")
    return jsonify({'message': 'Senha redefinida com sucesso!'}), 200
    
@usuario_bp.route('/perfil',methods=['GET'])
@jwt_required() #Garantir que a rota só possa ser acessada por usuários
#autenticados com um JWT válido.
def perfil():
    user_id=get_jwt_identity() #extrair a indentidade do usuario a partir do token JWT
    return jsonify({"msg":f"Bem-vindo ao perfil do usuario {user_id}!"})

@usuario_bp.route('/perfil_atualizar',methods=['PUT'])
@jwt_required()#Garantir que a rota só possa ser acessada por usuários
#autenticados com um JWT válido.
def atualizar_perfil():
    usuario_atual= get_jwt_identity()
    print(f"Usuario  no token:{usuario_atual}")
    #buscar o usuario no banco de dados
    usuario=Usuario.query.filter_by(role=usuario_atual).first()
    print(f"Usuário encontrado no banco: {usuario}")

    #verificar se o usuário existe no banco de dados
    if not usuario:
        return jsonify({'erro':" Usuário não encontrado"}),404
    #obter os dados enviados na requisição
    dados=request.json
    if not dados:
        return jsonify({"erro":"nenhum dado enviado."}),400
    try:
        #atualizar  os dados permitidos
    
        if 'nome' in dados:
            usuario.nome= dados["nome"]
        if 'email' in dados:
        #verifica se o email já está  em uso
            email_existente= Usuario.query.filter_by(email=dados["email"]).first()
            if email_existente and email_existente.id != usuario.id:
                return jsonify({"erro": "Email já está em uso"}), 400
            usuario.email = dados["email"]
        if 'senha' in dados:
            senha_clara=dados["senha"]
            senha_hash=generate_password_hash(senha_clara) #passa a senha para gerar hash
            usuario.senha=senha_hash
        db.session.commit()
        return jsonify({"mensagem":"Perfil atualizado com sucesso."}),200
    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        # Captura erros e retorna uma mensagem amigável
        return jsonify({"erro": f"Erro ao atualizar o perfil: {str(e)}"}), 500
    
@usuario_bp.route("/listar_endereços",methods=['GET'])
def listar_endereco():
    try:
        dados=Enderecos.query.all() #Recupere todos os endereços do banco
        if not dados:
            return jsonify({"mensagem":"Nenhum endereço encontrado"}),404
        #criar uma lista de endereços
        enderecos_lista=[]
        for endereco in dados:
            enderecos_lista.append({
                "usuario_id":endereco.usuario_id,
                "rua": endereco.rua,
                "numero": endereco.numero,
                "complemento":endereco.complemento,
                "bairro": endereco.bairro,
                "cidade": endereco.cidade,
                "estado": endereco.estado,
                "cep": endereco.cep
            })
        #retornar os dados no formato json
        return jsonify(enderecos_lista),200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar os endereços.", "detalhes": str(e)}), 500
    
    
@usuario_bp.route("/adicionar_enderecos",methods=['POST'])
def adicionar_endereco():
    dados=request.get_json()
    if not dados:
        return jsonify({"erro":"Nnehum dado json enviado"}),400
    campos_obrigatorio=['usuario_id','rua','numero','complemento','bairro','cidade','estado','cep']
    for campo in  campos_obrigatorio:
        if campo not in dados:
            return jsonify({"erro":f"Campo obrigatorio {campo} não foi encontrado"}),400
    # Criação do objeto Enderecos
    novo_endereco = Enderecos(
        usuario_id=dados['usuario_id'],
        rua=dados['rua'],
        numero=dados['numero'],
        complemento=dados['complemento'],
        bairro=dados['bairro'],
        cidade=dados['cidade'],
        estado=dados['estado'],
        cep=dados['cep']
    )
    try:
        # Adiciona e salva no banco de dados
        db.session.add(novo_endereco)
        db.session.commit()
        
        return jsonify({
            "mensagem": "Endereço adicionado com sucesso!",
            "endereco": {
                "usuario_id": novo_endereco.usuario_id,
                "rua": novo_endereco.rua,
                "numero": novo_endereco.numero,
                "complemento": novo_endereco.complemento,
                "bairro": novo_endereco.bairro,
                "cidade": novo_endereco.cidade,
                "estado": novo_endereco.estado,
                "cep": novo_endereco.cep
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()  # Reverte alterações em caso de erro
        return jsonify({"erro": "Erro ao salvar o endereço no banco de dados.", "detalhes": str(e)}), 500
    
@usuario_bp.route("/editar_endereço/<int:id>",methods=['PUT'])
def editar_endereço(id):
    #Buscar o endereço no banco de dados
    endereco=Enderecos.query.get(id)
    if not endereco:
        return jsonify({"erro":"Nenhum arquivo json encontrado"}),404
    # obter os dados da requisição
    dados=request.get_json()

    endereco.rua=dados.get("rua",endereco.rua)
    endereco.numero=dados.get("numero",endereco.rua)
    endereco.complemento=dados.get("complemento",endereco.rua)
    endereco.bairro=dados.get("bairro",endereco.rua)
    endereco.cidade=dados.get("cidade",endereco.rua)
    endereco.estado=dados.get("estado",endereco.rua)
    endereco.cep=dados.get("cep",endereco.rua)

    db.session.commit()

    return jsonify({'mensagem': 'Endereço atualizado com sucesso!'}), 200

@usuario_bp.route("/deletar_endereço/<int:id>",methods={'DELETE'})
def deletar_endereco(id):
    #buscar endereço no banco
    endereco=Enderecos.query.get(id)
    if not endereco:
        return jsonify({"Erro":"Nenhum endereço encontrado!"}),404
    db.session.delete(endereco)
    db.session.commit()
    return jsonify({"message":"Endereço deletado com sucesso!"}),200

    
    

    

