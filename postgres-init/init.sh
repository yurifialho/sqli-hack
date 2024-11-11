#!/bin/bash

set -ex 

psql -v ON_ERROR_STOP=1  --username "$POSTGRES_USER" morbidus <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS dblink;
EOSQL

psql -v ON_ERROR_STOP=1  --username "$POSTGRES_USER" morbidus <<-EOSQL
  -- Criar tabela de usuários
  CREATE TABLE IF NOT EXISTS usuarios (
      id SERIAL PRIMARY KEY,  -- Usa SERIAL para auto incremento no PostgreSQL
      username VARCHAR(255) NOT NULL UNIQUE,
      password VARCHAR(255) NOT NULL
  );

  -- Inserir alguns usuários de exemplo com senhas já hashadas
  INSERT INTO usuarios (username, password) VALUES 
  ('joao', '86232fc52644bdd06cdf42c3521627f1'), 
  ('maria', 'e10adc3949ba59abbe56e057f20f883e'), 
  ('pedro', '3fb00fb776351db4f46be3b69a679756'),
  ('admin', '86232fc52644bdd06cdf42c3521627f1');

  -- Criar tabela de flags
  CREATE TABLE IF NOT EXISTS flag (
      id SERIAL PRIMARY KEY,  -- Usa SERIAL para auto incremento no PostgreSQL
      valor VARCHAR(255) NOT NULL UNIQUE
  );

  INSERT INTO flag (valor) VALUES
  ('SACI{3413134123413}');
EOSQL