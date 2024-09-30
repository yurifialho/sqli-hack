-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Inserir alguns usuários de exemplo com senhas já hashadas
-- A senha "123456" foi usada para esses exemplos e está hashada com bcrypt
INSERT INTO usuarios (username, password) VALUES 
('joao', '123456'), 
('maria', '123456'), 
('pedro', '123456'); 


CREATE TABLE IF NOT EXISTS flag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO flag (valor) VALUES
('SACI{3413134123413}');