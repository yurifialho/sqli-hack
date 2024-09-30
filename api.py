from flask import Flask, request, jsonify
from flasgger import APISpec, Schema, Swagger
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import os

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

# Configurações para conexão com o MySQL
app.config['MYSQL_HOST'] = os.getenv("DB_HOST") or 'bd'
app.config['MYSQL_USER'] = os.getenv("DB_USER") or 'morbidus'
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASS") or 'marvel'
app.config['MYSQL_DB'] = os.getenv("DB_SCHEMA") or 'morbidus'

# Inicializa a conexão MySQL
mysql = MySQL(app)

# Lista para armazenar os usuários
usuarios = []


# -----------------------------------------------
#  ROTAS DO CRUD DA APLICACAO
# -----------------------------------------------


# Rota para listar todos os usuários (READ)
@app.route('/usuarios', methods=['GET'])
#@jwt_required()
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
     # Verificar as credenciais no banco de dados MySQL
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()

    lista_usuarios = [{'id': user[0], 'username': user[1]} for user in usuarios]
    return jsonify(lista_usuarios), 200

# Rota para obter um único usuário pelo username (READ)
@app.route('/usuarios/<username>', methods=['GET'])
#@jwt_required()
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
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username FROM usuarios WHERE username = %s", [username])
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({'id': user[0], 'username': user[1]}), 200
    return jsonify({'mensagem': 'Usuário não encontrado!'}), 404

# Rota para cadastrar um novo usuário (CREATE)
@app.route('/usuarios', methods=['POST'])
#@jwt_required()
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
    
    # Conectar e executar a inserção no banco de dados MySQL
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", ( novo_usuario['username'], novo_usuario['password']))
    mysql.connection.commit()
    cur.close()

    #for usuario in usuarios:
    #    if usuario['username'] == novo_usuario['username']:
    #        return jsonify({'mensagem': 'Usuário já existe!'}), 400
    
    
    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'}), 201

# Rota para atualizar um usuário (UPDATE)
@app.route('/usuarios/<username>', methods=['PUT'])
#@jwt_required()
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
    dados = request.json
    username = dados.get('username')
    password = dados.get('password')

    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE usuarios SET username = %s, password = %s WHERE username = %s", (username, password, username))
        mysql.connection.commit()
        return jsonify({'mensagem': 'Usuário atualizado com sucesso!'}), 200
    except:
        return jsonify({'mensagem': 'Erro ao atualizar o usuário!'}), 400
    finally:
        cur.close()

# Rota para deletar um usuário (DELETE)
@app.route('/usuarios/<username>', methods=['DELETE'])
#@jwt_required()
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
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE username = %s", [username])
        mysql.connection.commit()
        return jsonify({'mensagem': 'Usuário deletado com sucesso!'}), 200
    except:
        return jsonify({'mensagem': 'Erro ao deletar o usuário!'}), 400
    finally:
        cur.close()

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
    dados = request.json
    username = dados.get('username')
    password = dados.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE username = %s", [username])
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[2], password):  # user[2] é a coluna da senha
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    return jsonify({'mensagem': 'Nome de usuário ou senha incorretos!'}), 401

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
    dados = request.json
    username = dados.get('username')
    password = generate_password_hash(dados.get('password'))
    if not username or not password:
        return jsonify({'mensagem': 'Nome de usuário e senha são obrigatórios!'}), 400

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        return jsonify({'mensagem': 'Usuário registrado com sucesso!'}), 201
    except:
        return jsonify({'mensagem': 'Erro ao registrar usuário!'}), 400
    finally:
        cur.close()
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)