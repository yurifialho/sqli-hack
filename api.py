from flask import Flask, request, jsonify
from flasgger import APISpec, Schema, Swagger, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Morbidus API",
    "uiversion": 2,
}
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Chave secreta para assinar os tokens JWT
jwt = JWTManager(app)
swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Morbidus API",
            "version": "1.0",
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
    },)

# Lista para armazenar os usuários
usuarios = []


# -----------------------------------------------
#  ROTAS DO CRUD DA APLICACAO
# -----------------------------------------------


# Rota para listar todos os usuários (READ)
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    """
    Listar todos os usuários
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuários
    """
    return jsonify(usuarios), 200

# Rota para obter um único usuário pelo username (READ)
@app.route('/usuarios/<username>', methods=['GET'])
@jwt_required()
def obter_usuario(username):
    """
    Obter um usuário específico
    ---
    tags:
      - Usuarios
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: Nome do usuário a ser buscado
    responses:
      200:
        description: Usuário encontrado
      404:
        description: Usuário não encontrado
    """
    for usuario in usuarios:
        if usuario['username'] == username:
            return jsonify(usuario), 200
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

# Rota para cadastrar um novo usuário (CREATE)
@app.route('/usuarios', methods=['POST'])
@jwt_required()
def cadastrar_usuario():
    """
    Cadastrar um novo usuário
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        description: Dados do usuário
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuário cadastrado com sucesso
      400:
        description: Usuário já existe
    """
    novo_usuario = request.json
    
    for usuario in usuarios:
        if usuario['username'] == novo_usuario['username']:
            return jsonify({'mensagem': 'Usuário já existe!'}), 400
    
    usuarios.append({
        'username': novo_usuario['username'],
        'password': novo_usuario['password']
    })
    
    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'}), 201

# Rota para atualizar um usuário (UPDATE)
@app.route('/usuarios/<username>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(username):
    """
    Atualizar um usuário
    ---
    tags:
      - Usuarios
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: Nome do usuário a ser atualizado
      - name: body
        in: body
        required: true
        description: Dados atualizados do usuário
        schema:
          type: object
          properties:
            password:
              type: string
    responses:
      200:
        description: Usuário atualizado com sucesso
      404:
        description: Usuário não encontrado
    """
    dados_atualizados = request.json
    
    for usuario in usuarios:
        if usuario['username'] == username:
            usuario['password'] = dados_atualizados.get('password', usuario['password'])
            return jsonify({'mensagem': 'Usuário atualizado com sucesso!'}), 200
    
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

# Rota para deletar um usuário (DELETE)
@app.route('/usuarios/<username>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(username):
    """
    Deletar um usuário
    ---
    tags:
      - Usuarios
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: Nome do usuário a ser deletado
    responses:
      200:
        description: Usuário deletado com sucesso
      404:
        description: Usuário não encontrado
    """
    for usuario in usuarios:
        if usuario['username'] == username:
            usuarios.remove(usuario)
            return jsonify({'mensagem': 'Usuário deletado com sucesso!'}), 200
    
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

# -----------------------------------------------
#  ROTAS HOME
# -----------------------------------------------

# Rota principal para verificar se o servidor está rodando
@app.route('/')
def home():
    """
    Verificação de status da API
    ---
    tags:
      - Home
    responses:
      200:
        description: A API está funcionando
    """
    return "Bem Vindo ao Morbidus - A API da última fronteira!", 200

# -----------------------------------------------
#  ROTAS DE AUTENTICACAO
# -----------------------------------------------

# Rota de login para gerar o token JWT
@app.route('/login', methods=['POST'])
def login():
    """
    Fazer login para obter o token JWT
    ---
    tags:
      - Autenticacao
    parameters:
      - name: body
        in: body
        required: true
        description: Dados de login
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login bem-sucedido
      401:
        description: Credenciais inválidas
    """
    dados_login = request.json
    username = dados_login.get('username')
    password = dados_login.get('password')

    # Verifica se o usuário existe e se a senha está correta
    for usuario in usuarios:
        if usuario['username'] == username and check_password_hash(usuario['password'], password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
    
    return jsonify({'mensagem': 'Credenciais inválidas'}), 401

# Rota para registro de novos usuários (sem necessidade de autenticação)
@app.route('/register', methods=['POST'])
def registrar_usuario():
    """
    Registrar um novo usuário
    ---
    tags:
      - Autenticacao
    parameters:
      - name: body
        in: body
        required: true
        description: Dados do usuário
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuário registrado com sucesso
      400:
        description: Usuário já existe
    """
    novo_usuario = request.json
    username = novo_usuario.get('username')
    password = novo_usuario.get('password')

    # Verifica se o username já existe
    for usuario in usuarios:
        if usuario['username'] == username:
            return jsonify({'mensagem': 'Usuário já existe!'}), 400
    
    # Adiciona o novo usuário com senha criptografada
    usuarios.append({
        'username': username,
        'password': generate_password_hash(password)
    })
    
    return jsonify({'mensagem': 'Usuário registrado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(debug=True)