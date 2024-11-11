#! /usr/bin/python
#
# @author Yuri Fialho
# @since 30/09/2024
#
# ------------------------------------------------------------
# API EDUCATIVA PARA VULNERABILIDADES DO TIPO SQL INJECTIONS
# ------------------------------------------------------------

from flask import Flask, request, jsonify
from flasgger import APISpec, Schema, Swagger
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from connection import OraConnection, MysqlConnection, PgConnection
import os
import hashlib

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


# Inicializa a conexão com o banco de dados

db_connection = None
db_host = os.getenv("DB_HOST") or 'bd'
db_user = os.getenv("DB_USER") or 'morbidus'
db_pass = os.getenv("DB_PASS") or 'marvel'
db_data = os.getenv("DB_SCHEMA") or 'morbidus'

database_type = os.getenv("DATABASE_TYPE") or 'MYSQL'

if database_type == 'MYSQL':
  print("Using MYSQL Database")
  # Configurações para conexão com o MySQL
  app.config['MYSQL_HOST'] = db_host
  app.config['MYSQL_USER'] = db_user
  app.config['MYSQL_PASSWORD'] = db_pass
  app.config['MYSQL_DB'] = db_data

  db_connection = MysqlConnection(app)

elif database_type == 'ORACLE':
  print("Using ORACLE Database")
  db_connection = OraConnection(db_host, db_data, db_user, db_pass)

elif database_type == "POSTGRES":
  db_connection = PgConnection(db_host, db_data, db_user, db_pass)  


def string_para_md5(texto):
    # Cria o objeto hash MD5
    md5_hash = hashlib.md5()
    # Codifica a string para bytes e atualiza o hash
    md5_hash.update(texto.encode('utf-8'))
    # Retorna o hash em formato hexadecimal
    return md5_hash.hexdigest()

# -----------------------------------------------
#  ROTAS DO CRUD DA APLICACAO
# -----------------------------------------------


# Rota para listar todos os usuários (READ)
# Exemplo: curl --location 'http://localhost:5000/usuarios' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzcwOTQ3OSwianRpIjoiNGY0NjI5YmQtN2I0OS00ZjJiLThmZDMtNTVmZGM0OTA3MDJiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1hcmlhIiwibmJmIjoxNzI3NzA5NDc5LCJjc3JmIjoiZGEyYTgxN2ItNzZkMC00ZDU3LTk5MjItNzM1MTBlYjhmOGRhIiwiZXhwIjoxNzI3NzEwMzc5fQ.v8qEuSBy_6JLg4paOMB2WLexsC342BTXEfRGKIj-UmY'
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
     # Verificar as credenciais no banco de dados MySQL
    usuarios = db_connection.get_all("SELECT id, username FROM usuarios")
    lista_usuarios = [{'id': user[0], 'username': user[1]} for user in usuarios]
    return jsonify(lista_usuarios), 200

# Rota para obter um único usuário pelo username (READ)
# Url Vunerável: curl --location 'http://localhost:5000/usuarios/'\'' or 1=1 or '\''' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzcxMDQzNywianRpIjoiNmE3OTc0MzItYjk5OS00OTY4LTljNDAtYTYwZGU5YTNmOTkxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1hcmlhIiwibmJmIjoxNzI3NzEwNDM3LCJjc3JmIjoiNDdkYmQ3ZDQtYzU0Yy00YmIwLThlODYtNDNhM2IwOWIwNzA0IiwiZXhwIjoxNzI3NzExMzM3fQ.U6fyUtpJaAtjTxZbAWwSRHmTFscVUsp6OJNy2xDTN6A'

# ORACLE
# Url Vunerável: curl --location 'http://localhost:5000/usuarios/'\'' union all SELECT 1, user FROM dual --' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzcxMDQzNywianRpIjoiNmE3OTc0MzItYjk5OS00OTY4LTljNDAtYTYwZGU5YTNmOTkxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1hcmlhIiwibmJmIjoxNzI3NzEwNDM3LCJjc3JmIjoiNDdkYmQ3ZDQtYzU0Yy00YmIwLThlODYtNDNhM2IwOWIwNzA0IiwiZXhwIjoxNzI3NzExMzM3fQ.U6fyUtpJaAtjTxZbAWwSRHmTFscVUsp6OJNy2xDTN6A'

# POSTGRES
# curl --location 'http://localhost/usuarios/'\'' union all SELECT 1, current_database()  --' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTI5MTk1OCwianRpIjoiNDJkODM3ZGMtNWFmYi00N2I2LThkYmItYjc4MjMxMGVjNDIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1hcmlhIiwibmJmIjoxNzMxMjkxOTU4LCJjc3JmIjoiZDdkMDk3ZGQtM2YyOS00MDk0LTkxYTctNTc0Zjg5NjNiMjI3IiwiZXhwIjoxNzMxMjkyODU4fQ.3HPAr5hrxrnXh-RE1pv5ZqrCOK2dJ75TNCcTr3HBYaY'
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
    user = db_connection.get_one("SELECT id, username FROM usuarios WHERE username = '"+username+"'", [])
    if user:
        return jsonify({'id': user[0], 'username': user[1]}), 200
    return jsonify({'mensagem': 'Usuário não encontrado!'}), 404

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
    
    # Conectar e executar a inserção no banco de dados MySQL
    db_connection.alter("INSERT INTO usuarios (username, password) VALUES (%s, %s)", ( novo_usuario['username'], novo_usuario['password']))    
    
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
    dados = request.json
    username = dados.get('username')
    password = string_para_md5(dados.get('password'))

    try:
        db_connection.alter("UPDATE usuarios SET username = %s, password = %s WHERE username = %s", (username, password, username))
        return jsonify({'mensagem': 'Usuário atualizado com sucesso!'}), 200
    except:
        return jsonify({'mensagem': 'Erro ao atualizar o usuário!'}), 400

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
    try:
        db_connection.alter("DELETE FROM usuarios WHERE username = %s", [username])
        return jsonify({'mensagem': 'Usuário deletado com sucesso!'}), 200
    except:
        return jsonify({'mensagem': 'Erro ao deletar o usuário!'}), 400

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
    return "Bem Vindo ao Morbidus - A API da última fronteira! by Maria Fca.", 200

# -----------------------------------------------
#  ROTAS DE AUTENTICACAO
# -----------------------------------------------

# Rota de login para gerar o token JWT
# Exemplo: curl --location 'http://localhost:5000/login' --header 'Content-Type: application/json' --data '{ "password": "123456","username": "maria"}'
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
    password = string_para_md5(dados.get('password'))

    user = db_connection.get_one("SELECT * FROM usuarios WHERE username = %s", [username])
    if user and user[2] == password:  # user[2] é a coluna da senha
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    return jsonify({'mensagem': 'Nome de usuário ou senha incorretos!'}), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)