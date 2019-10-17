from fastapi import FastAPI
import pymysql


app = FastAPI()


def connect_db(host='localhost',user='root',password='MegaDados',database='rede_passaros'):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='rafavr98',
        database='rede_passaros')
    return connection

@app.put('/user')
def insert_user(nome: str,email: str,cidade: str):
    connection = connect_db()
    with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES (%s, %s,%s)''',(nome,email,cidade))
            cursor.execute('''COMMIT''')
    connection.close()

@app.put('/post')
def insert_post(titulo,texto,img_url,usr_id):
    connection = connect_db()
    with connection.cursor() as cursor:
            cursor.execute('''START TRANSACTION''')
            cursor.execute('''INSERT INTO Posts 
                    (titulo,texto,img_url,ativo,usr_id)
                     VALUES 
                     (%s, %s,%s,True,%s)''',(titulo,texto,img_url,usr_id))
            cursor.execute('''SELECT LAST_INSERT_ID()''')
            postid = cursor.fetchone()[0]
            cursor.execute('''SELECT id FROM Usuarios''')
            userid_list = cursor.fetchall()
            for u in userid_list:
                cursor.execute('''INSERT INTO Gosta_post 
                        (usr_id, post_id, gostou, ativo)
                        VALUES 
                        (%s, %s,%s,%s)''',(u,postid,0,0))
            lista_palavras = texto.split()
            for palavra in lista_palavras:
                if '@' in palavra:
                    usuario = palavra.translate({ord('@'): None})
                    cursor.execute('''SELECT id FROM Usuarios WHERE nome = %s''',(usuario))
                    userid = cursor.fetchone()[0]
                    cursor.execute('''INSERT INTO Menciona_usr(usr_id,post_id,ativo) VALUES (%s,%s,True)''',(userid,postid))
                if '#' in palavra:
                    passaro = palavra.translate({ord('#'): None})
                    cursor.execute('''INSERT INTO Menciona_pass(post_id,pass_id,ativo) VALUES (%s,%s,True)''',(postid,passaro))
            cursor.execute('''COMMIT''')
    connection.close()

@app.put('/passaro/{especie}')
def insert_passaro(especie):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''INSERT INTO Passaros
                            (especie)
                            VALUES 
                            (%s)''',(especie))
        cursor.execute('''COMMIT''')
    connection.close()

@app.put('/preferencia')
def insert_preferencia(user_id,especie):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''INSERT INTO Preferencia(usr_id,pass_id) VALUES (%s,%s)''',(user_id,especie))
        cursor.execute('''COMMIT''')
    connection.close()

@app.get('/preferencia/{user_id}')
def pega_preferencia(user_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''SELECT pass_id FROM Preferencia WHERE usr_id = %s''',(user_id))
        pass_pref = cursor.fetchall()
    return pass_pref
    connection.close()

@app.put('/view')
def insert_view(usr_id,post_id,aparelho,browser,ip,horario):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''INSERT INTO Views(usr_id,post_id,aparelho,browser,ip,horario) VALUES (%s,%s,%s,%s,%s,%s)''',(usr_id,post_id,aparelho,browser,ip,horario))
        cursor.execute('''COMMIT''')
    connection.close()

@app.get('/user/{usr_id}')
def busca_usr(usr_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''CALL busca_usr(%s);''',(usr_id))
        user_info = cursor.fetchone()
    user = {
        "nome": user_info[0],
        "email": user_info[1],
        "cidade": user_info[2]
    }
    return user

@app.post('/like/{usr_id},{post_id}')
def like_deslike_post(usr_id, post_id, likeOrDeslike, ativo=1):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''UPDATE Gosta_post SET gostou=%s, ativo=%s WHERE usr_id=%s and post_id=%s''', (likeOrDeslike, ativo, usr_id, post_id))
        cursor.execute('''COMMIT''')

@app.post('/unlike/{usr_id},{post_id}')
def unlike_undeslike_post(usr_id, post_id, ativo=0):
    connection = connect_db() 
    with connection.cursor() as cursor:
        cursor.execute('''UPDATE Gosta_post SET ativo=%s WHERE usr_id=%s and post_id=%s''',  (ativo, usr_id, post_id))
        cursor.execute('''COMMIT''')

@app.get('/posts/{usr_id}')
def lista_usr_posts(usr_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''CALL busca_post(%s);''',(usr_id))
        return cursor.fetchall()

@app.delete('/posts/{post_id}')
def delete_post(post_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''CALL delete_post(%s);''',(post_id))
        cursor.execute('''COMMIT''')

@app.get('/view')
def busca_cross_mobile_browser():
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''SELECT aparelho, browser, COUNT(*) FROM Views GROUP BY aparelho, browser''')
        cross_table = cursor.fetchall()
    return cross_table
        
@app.get('/users/{user_id}')
def users_mencionam_user(user_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT Posts.usr_id FROM Posts 
        INNER JOIN Menciona_usr ON id = Menciona_usr.post_id 
        WHERE Menciona_usr.usr_id = %s
        GROUP BY usr_id ''',(user_id))
        users = []
        for user in cursor.fetchall():
            users.append(user[0])
    return users
        
            
@app.get('/popular/{cidade}')
def user_mais_popular(cidade):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''
                SELECT usr_id
                FROM Menciona_usr
                INNER JOIN Usuarios ON usr_id = Usuarios.id
                WHERE Usuarios.cidade = %s AND ativo = True
                GROUP BY usr_id
                ORDER BY COUNT(usr_id) DESC
                LIMIT 1 ''',cidade)
        pop = cursor.fetchone()
        if pop is None:
            return None
        else:
            return pop[0]



@app.get('/image_url')
def busca_cross_imgurl_pass():
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''SELECT img_url, Menciona_pass.pass_id , COUNT(*)
                        FROM Posts 
                        INNER JOIN Menciona_pass ON id=Menciona_pass.post_id
                        WHERE Menciona_pass.ativo = 1 
                        GROUP BY img_url, Menciona_pass.pass_id''')
        cross_table = cursor.fetchall()
    return cross_table





