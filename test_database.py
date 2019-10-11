import unittest
import subprocess
from subprocess import Popen, PIPE, STDOUT
from functools import partial
import pymysql
import datetime

def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)

class TestPassaroDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # SQL credentials
        user = 'root'
        password = '-pMegaDados'

        # Create database if necessary
        session = subprocess.Popen(['mysql','-u',user,password],stdin=PIPE,stderr=PIPE,stdout=PIPE)
        f = open('cria_base.sql','rb')
        b_cmd = f.read()
        session.stdin.write(b_cmd)
        stdout, stderr = session.communicate()
        f.close()

        cls.connection = pymysql.connect(
        host='localhost',
        user='root',
        password='MegaDados',
        database='rede_passaros')


    @classmethod
    def tearDownClass(cls):
        cls.connection.close()


    def test_insert_usuario(self):

        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES ('rafael', 'rafael@gmail.com','sao paulo')''')
            cursor.execute('''SELECT nome,email,cidade from Usuarios WHERE nome="rafael" ''')
                
            self.assertEqual(cursor.fetchone(),(('rafael', 'rafael@gmail.com','sao paulo')))
            cursor.execute('''COMMIT''')

    def test_insert_post(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES ('rafael Vieira', 'rafael@gmail.com','sao paulo capital')''')
            cursor.execute('''INSERT INTO Posts 
                    (titulo,texto,img_url,ativo,usr_id)
                     VALUES 
                     ('Por hj é só pessoal', 'tem um passaro na minha janela','passarao.com/passarinho.img',True,2)''')
            cursor.execute('''SELECT titulo,texto,img_url,ativo,usr_id from Posts WHERE titulo='Por hj é só pessoal' ''')
            self.assertEqual(cursor.fetchone(),(('Por hj é só pessoal', 'tem um passaro na minha janela','passarao.com/passarinho.img',True,2)))
            cursor.execute('''COMMIT''')
    
    def test_insert_passaro(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Passaros
                            (especie)
                            VALUES 
                            ("faisão")''')
            cursor.execute('''SELECT especie from Passaros WHERE especie="faisão" ''')
                
            self.assertEqual(cursor.fetchone()[0],'faisão')
            cursor.execute('''COMMIT''')

    def test_delete_post(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES ('Rafael Vieira', 'rafael@gmail.com','sao paulo capital')''')
            cursor.execute('''INSERT INTO Passaros (especie) VALUES ("canarinho") ''')
            cursor.execute('''INSERT INTO Posts 
                    (titulo,texto,img_url,ativo,usr_id)
                        VALUES 
                        ('NOVO PASSARO', 'tem um passaro na minha janela','passarao.com/passarinho.img',TRUE,1)''')
            cursor.execute('''INSERT INTO Menciona_usr (usr_id, post_id, ativo) VALUES (1, 1,TRUE)''')
            cursor.execute('''INSERT INTO Menciona_pass (post_id, pass_id, ativo) VALUES (1, "canarinho",TRUE)''')

            cursor.execute('''UPDATE Posts SET ativo=FALSE WHERE usr_id=1''')

            cursor.execute('''SELECT ativo FROM Menciona_pass WHERE post_id=1''')
            self.assertEqual(cursor.fetchone()[0],False)
            
            cursor.execute('''SELECT ativo FROM Menciona_usr WHERE usr_id=1''')
            self.assertEqual(cursor.fetchone()[0],False)

            cursor.execute('''SELECT ativo FROM Posts WHERE usr_id=1''')
            self.assertEqual(cursor.fetchone()[0],False)
            
            cursor.execute('''COMMIT''')

    def test_insert_preferencia(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES ('Rafael Vieira', 'rafael@gmail.com','sao paulo capital')''')
            cursor.execute('''INSERT INTO Passaros (especie) VALUES ('bem-te-vi')''')
            cursor.execute('''INSERT INTO Preferencia(usr_id,pass_id) VALUES (3,'bem-te-vi')''')
            cursor.execute('''SELECT usr_id, pass_id from Preferencia WHERE usr_id=3 AND pass_id='bem-te-vi' ''')
            
            self.assertEqual(cursor.fetchone(),(3, 'bem-te-vi'))
            cursor.execute('''COMMIT''')
            
    def test_insert_menciona_usr(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES ('Gabriel M', 'gabriel@gmail.com','sao paulo capital')''')
            cursor.execute('''INSERT INTO Posts 
                    (titulo,texto,img_url,ativo,usr_id)
                     VALUES 
                     ('Novidades', 'Adicionando amigo ao grupo','amigo.com/amigo.img',TRUE,3)''')


            cursor.execute('''INSERT INTO Menciona_usr(usr_id,post_id,ativo) VALUES (3,3,TRUE)''')
            cursor.execute('''SELECT usr_id, post_id, ativo from Menciona_usr WHERE usr_id=3 AND post_id=3 AND ativo=True ''')
            
            self.assertEqual(cursor.fetchone(),(3, 3, True))
            cursor.execute('''COMMIT''')

    def test_insert_menciona_pass(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES ('Gabriel M', 'gabriel@gmail.com','sao paulo capital')''')
            cursor.execute('''INSERT INTO Passaros (especie) VALUES ('joao de barro')''')
            cursor.execute('''INSERT INTO Posts 
                    (titulo,texto,img_url,ativo,usr_id)
                     VALUES 
                     ('Novidades2', 'Adicionando passaro ao grupo','pass.com/pass.img',True,2)''')


            cursor.execute('''INSERT INTO Menciona_pass(pass_id,post_id,ativo) VALUES ('joao de barro',2,True)''')
            cursor.execute('''SELECT pass_id, post_id, ativo from Menciona_pass WHERE pass_id='joao de barro' AND post_id=2 AND ativo=True ''')
            self.assertEqual(cursor.fetchone(),('joao de barro', 2, True))
            cursor.execute('''COMMIT''')

    def test_insert_view(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO Usuarios (nome,email,cidade) VALUES ('Gabriel M2', 'gabriel2@gmail.com','sao paulo capital')''')
            cursor.execute('''INSERT INTO Posts 
                        (titulo,texto,img_url,ativo,usr_id)
                            VALUES 
                            ('Mais um post', 'tem um passaro na minha janela','passarao.com/passarinho.img',TRUE,3)''')
            cursor.execute('''INSERT INTO Views(usr_id,post_id,aparelho,browser,ip,horario) VALUES (3,5,'Sumsang','Opera','192.168.0.0','2012-06-18 10:34:09')''')
            cursor.execute('''SELECT aparelho, browser, ip, horario from Views WHERE usr_id=3 AND post_id=5''')
            self.assertEqual(cursor.fetchone(),('Sumsang', 'Opera', '192.168.0.0', datetime.datetime(2012, 6, 18, 10, 34, 9)))

if __name__ == '__main__':
    unittest.main()