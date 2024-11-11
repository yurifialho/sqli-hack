import cx_Oracle
from flask_mysqldb import MySQL
import psycopg2
from psycopg2 import sql

class OraConnection:

  def __init__(self, host='db', sdi='orcl', user='system', password='oracle') -> None:
    self.connection = cx_Oracle.connect(user=user, password=password, dsn=host+"/"+sdi)
    cursor = self.connection.cursor()
    cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = SYS")


  def alter(self, query, params):
    query = self.replace_placeholders(query)
    cursor = self.connection.cursor()
    cursor.execute(query, params)

  def get_all(self, query):
    query = self.replace_placeholders(query)
    cursor = self.connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

  def get_one(self, query, params):
    query = self.replace_placeholders(query)
    cursor = self.connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row
  
  # Deixa os parâmetros no padrão do oracle 
  def replace_placeholders(self, query):
    count = 1
    while '%s' in query:
        query = query.replace('%s', f':{count}', 1)
        count += 1
    return query

class MysqlConnection:

  def __init__(self, app) -> None:
    self.mysql = MySQL(app)

  def alter(self, query, params):
    cursor = self.mysql.connection.cursor()
    cursor.execute(query, params)

  def get_all(self, query):
    cursor = self.mysql.connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

  def get_one(self, query, params):
    cursor = self.mysql.connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row

class PgConnection:

  def __init__(self, host='db', database='morbidus', user='morbidus', password='marvel') -> None:
    self.connection = psycopg2.connect(
        dbname=database,  # Substitua pelo nome do banco
        user=user,          # Substitua pelo seu usuário
        password=password,        # Substitua pela sua senha
        host=host,        # Substitua se o banco não estiver local
        port="5432"              # Porta padrão do PostgreSQL
    )
    self.connection.autocommit = True

  def alter(self, query, params):
    cursor = self.connection.cursor()
    cursor.execute(query, params)
    

  def get_all(self, query):
    cursor = self.connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

  def get_one(self, query, params):
    cursor = self.connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row