-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Inserir alguns usuários de exemplo com senhas já hashadas
INSERT INTO usuarios (username, password) VALUES 
('joao', '86232fc52644bdd06cdf42c3521627f1'), 
('maria', 'e10adc3949ba59abbe56e057f20f883e'), 
('pedro', '3fb00fb776351db4f46be3b69a679756'),
('admin', '86232fc52644bdd06cdf42c3521627f1');
 


CREATE TABLE IF NOT EXISTS flag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO flag (valor) VALUES
('SACI{3413134123413}');