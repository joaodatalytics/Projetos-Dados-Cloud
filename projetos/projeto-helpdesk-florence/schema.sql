CREATE DATABASE florence_db;
USE florence_db;
CREATE TABLE chamados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_funcionario VARCHAR(100) NOT NULL,
    setor VARCHAR(50) NOT NULL,
    prioridade VARCHAR(20) NOT NULL,
    descricao TEXT NOT NULL,
    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);