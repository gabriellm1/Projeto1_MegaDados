
USE rede_passaros;
DROP TABLE IF EXISTS Gosta_post;
CREATE TABLE Gosta_post(usr_id INT, post_id INT, gostou BOOLEAN, ativo BOOLEAN, FOREIGN KEY(usr_id) REFERENCES Usuarios(id), FOREIGN KEY(post_id) REFERENCES Posts(id), PRIMARY KEY(usr_id, post_id));
ALTER TABLE Views DROP PRIMARY KEY, ADD PRIMARY KEY (usr_id, post_id, horario);

DROP TRIGGER IF EXISTS trig_usr_post;
DELIMITER //
CREATE TRIGGER trig_usr_post 
BEFORE UPDATE ON Posts
FOR EACH ROW
BEGIN
	IF NEW.ativo = FALSE THEN
		UPDATE Menciona_usr
			SET ativo = FALSE WHERE OLD.id = Menciona_usr.post_id;
		UPDATE Menciona_pass
			SET ativo = FALSE WHERE OLD.id = Menciona_pass.post_id;
		UPDATE Gosta_post
			SET ativo = FALSE WHERE OLD.id = Gosta_post.post_id;
	END IF;
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS busca_usr;
DELIMITER //
CREATE PROCEDURE busca_usr(IN usr_id INT)
BEGIN
	SELECT nome,email,cidade
	FROM Usuarios
	WHERE id = usr_id;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS busca_post;
DELIMITER //
CREATE PROCEDURE busca_post(IN user_id INT)
BEGIN
	SELECT titulo,texto,img_url
	FROM Posts
	WHERE usr_id = user_id AND ativo = True
	order by id DESC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS delete_post;
DELIMITER //
CREATE PROCEDURE delete_post(IN post_id INT)
BEGIN
	UPDATE Posts SET ativo=FALSE WHERE id=post_id;
END //
DELIMITER ;





