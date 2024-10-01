-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Inserir alguns usuários de exemplo com senhas já hashadas
INSERT INTO usuarios (username, password) VALUES 
('joao', '1#6A26Zw%kQgq!i$*g0ntu&zKP'), 
('maria', 'a1&KWLEQiBd^9ZUM5o1N9H*u#P'), 
('pedro', 'FPhqbk&0*3n7#CL63zAISqUu^A'),
('admin', '123456');
 


CREATE TABLE IF NOT EXISTS flag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO flag (valor) VALUES
('SACI{3413134123413}');
