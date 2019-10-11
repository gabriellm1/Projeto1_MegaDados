DROP DATABASE IF EXISTS rede_passaros;
CREATE DATABASE rede_passaros;
USE rede_passaros;
CREATE TABLE Usuarios(id INT AUTO_INCREMENT, nome VARCHAR(50), email VARCHAR(80), cidade VARCHAR(50), PRIMARY KEY(id));
CREATE TABLE Posts(id iNT AUTO_INCREMENT, titulo VARCHAR(50) NOT NULL, texto VARCHAR(300), img_url VARCHAR(100), ativo BOOLEAN, usr_id INT, PRIMARY KEY(id), FOREIGN KEY(usr_id) REFERENCES Usuarios(id));
CREATE TABLE Passaros(especie VARCHAR(50), PRIMARY KEY(especie));
CREATE TABLE Preferencia(usr_id INT, pass_id VARCHAR(50), FOREIGN KEY(usr_id) REFERENCES Usuarios(id), FOREIGN KEY(pass_id) REFERENCES Passaros(especie), PRIMARY KEY(usr_id, pass_id));
CREATE TABLE Menciona_pass(post_id INT, pass_id VARCHAR(50), ativo BOOLEAN, FOREIGN KEY(post_id) REFERENCES Posts(id), FOREIGN KEY(pass_id) REFERENCES Passaros(especie), PRIMARY KEY(post_id, pass_id));
CREATE TABLE Menciona_usr(usr_id INT, post_id INT, ativo BOOLEAN, FOREIGN KEY(usr_id) REFERENCES Usuarios(id), FOREIGN KEY(post_id) REFERENCES Posts(id), PRIMARY KEY(usr_id, post_id));
CREATE TABLE Views(usr_id INT, post_id INT, aparelho VARCHAR(20), browser VARCHAR(20), ip VARCHAR(50), horario DATETIME, FOREIGN KEY(usr_id) REFERENCES Usuarios(id), FOREIGN KEY(post_id) REFERENCES Posts(id), PRIMARY KEY(usr_id, post_id));

DROP TRIGGER IF EXISTS trig_usr_post;
DELIMITER //
CREATE TRIGGER trig_usr_post 
BEFORE UPDATE ON Posts
FOR EACH ROW
BEGIN
	IF NEW.ativo = FALSE THEN
		UPDATE Menciona_usr 
			SET ativo = FALSE;
		UPDATE Menciona_pass
			SET ativo = FALSE;
	END IF;
END//
DELIMITER ;