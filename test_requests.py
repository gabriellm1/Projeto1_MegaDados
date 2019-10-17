import unittest
import subprocess
from subprocess import Popen, PIPE, STDOUT
from functools import partial
import pymysql
import datetime
import requests
from time import sleep

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
        password = '-prafavr98'

        # Create database if necessary
        session = subprocess.Popen(['mysql','-u',user,password],stdin=PIPE,stderr=PIPE,stdout=PIPE)
        f = open('cria_base.sql','rb')
        b_cmd = f.read()
        session.stdin.write(b_cmd)
        stdout, stderr = session.communicate()
        f.close()

        # Run Delta script
        session = subprocess.Popen(['mysql','-u',user,password],stdin=PIPE,stderr=PIPE,stdout=PIPE)
        f = open('script_delta.sql','rb')
        b_cmd = f.read()
        session.stdin.write(b_cmd)
        stdout, stderr = session.communicate()
        f.close()

        cls.connection = pymysql.connect(
        host='localhost',
        user='root',
        password='rafavr98',
        database='rede_passaros')


    @classmethod
    def tearDownClass(cls):
        cls.connection.close()


    def test_a_usuario(self):
        r = requests.put("http://127.0.0.1:8000/user?nome=hugo&email=%40&cidade=sp")
        self.assertEqual(r.status_code,200)
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT nome,email,cidade from Usuarios WHERE nome="hugo" ''')
            self.assertEqual(cursor.fetchone(),(('hugo', '@','sp')))
            cursor.execute('''COMMIT''')    

    def test_b_insert_passaro(self):
        r = requests.put("http://127.0.0.1:8000/passaro/bemtevi")
        self.assertEqual(r.status_code,200)
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT * from Passaros''')
            self.assertEqual(cursor.fetchone()[0],"bemtevi")
            cursor.execute('''COMMIT''')
    
    def test_c_insert_post(self):
        r = requests.put("http://127.0.0.1:8000/post?titulo=teste&texto=%40hugo%20%23bemtevi&img_url=q&usr_id=1")
        self.assertEqual(r.status_code,200)
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT titulo,texto,img_url,ativo,usr_id from Posts WHERE titulo='teste' ''')
            self.assertEqual(cursor.fetchone(),(('teste', '@hugo #bemtevi','q',1,1)))
            cursor.execute('''COMMIT''')


    def test_d_delete_post(self):
        r = requests.delete("http://127.0.0.1:8000/posts/1")
        self.assertEqual(r.status_code,200)
        with self.connection.cursor() as cursor:

            cursor.execute('''SELECT ativo FROM Menciona_pass WHERE post_id=1''')
            self.assertEqual(cursor.fetchone()[0],False)
            
            cursor.execute('''SELECT ativo FROM Menciona_usr WHERE post_id=1''')
            self.assertEqual(cursor.fetchone()[0],False)

            cursor.execute('''SELECT ativo FROM Posts WHERE id=1''')
            self.assertEqual(cursor.fetchone()[0],False)
            cursor.execute('''COMMIT''')

    def test_e_preferencia(self):
        r = requests.put("http://127.0.0.1:8000/preferencia?user_id=1&especie=bemtevi")
        self.assertEqual(r.status_code,200)
        r = requests.get("http://127.0.0.1:8000/preferencia/1")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json()[0][0],"bemtevi")

    def test_f_view(self):
        r = requests.put("http://127.0.0.1:8000/view?usr_id=1&post_id=1&aparelho=Samsung&browser=Chrome&ip=1234567890&horario=2012-06-18%2010%3A34%3A09")
        self.assertEqual(r.status_code,200)  
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT aparelho, browser, ip, horario from Views WHERE usr_id=1 AND post_id=1''')
            self.assertEqual(cursor.fetchone(),('Samsung', 'Chrome', '1234567890', datetime.datetime(2012, 6, 18, 10, 34, 9)))
            cursor.execute('''COMMIT''')

    def test_g_cross_table_views(self):
        r = requests.put("http://127.0.0.1:8000/view?usr_id=1&post_id=1&aparelho=Samsung&browser=Chrome&ip=1234567890&horario=2012-06-19%2010%3A34%3A09")
        r1 = requests.put("http://127.0.0.1:8000/view?usr_id=1&post_id=1&aparelho=Samsung&browser=Edge&ip=1234567890&horario=2012-06-20%2010%3A34%3A09")
        r2 = requests.put("http://127.0.0.1:8000/view?usr_id=1&post_id=1&aparelho=iPhone&browser=Chrome&ip=1234567890&horario=2012-06-21%2010%3A34%3A09")
        r3 = requests.put("http://127.0.0.1:8000/view?usr_id=1&post_id=1&aparelho=iPhone&browser=Safari&ip=1234567890&horario=2012-06-22%2010%3A34%3A09")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r1.status_code,200)
        self.assertEqual(r2.status_code,200)
        self.assertEqual(r3.status_code,200)
        r = requests.get("http://127.0.0.1:8000/view")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[['Samsung', 'Chrome', 2], ['Samsung', 'Edge', 1], ['iPhone', 'Chrome', 1], ['iPhone', 'Safari', 1]])

    def test_h_users_mencionam_user(self):
        r0 = requests.put("http://127.0.0.1:8000/passaro/canario")
        r = requests.put("http://127.0.0.1:8000/user?nome=rafa&email=%40&cidade=sp")
        r1 = requests.put("http://127.0.0.1:8000/user?nome=leite&email=%40&cidade=sp")
        r2 = requests.put("http://127.0.0.1:8000/post?titulo=teste&texto=%40rafa%20%23bemtevi&img_url=z&usr_id=1")
        r3 = requests.put("http://127.0.0.1:8000/post?titulo=teste&texto=%40rafa%20%23canario&img_url=z&usr_id=3")
        self.assertEqual(r0.status_code,200)
        self.assertEqual(r.status_code,200)
        self.assertEqual(r1.status_code,200)
        self.assertEqual(r2.status_code,200)
        self.assertEqual(r3.status_code,200)
        r = requests.get("http://127.0.0.1:8000/users/2")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[1,3])

    def test_i_popular(self):
        r = requests.get("http://127.0.0.1:8000/popular/sp")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),2)

    def test_j_cross_table_imgurl_tags(self):
        r = requests.get("http://127.0.0.1:8000/image_url")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[["z","bemtevi",1],["z","canario",1]])

    def test_k_lista_posts_usrs(self):
        r = requests.put("http://127.0.0.1:8000/post?titulo=esse%20foi%20o%20ultimo&texto=ultimo%20q%20eu%20fiz&img_url=bla&usr_id=3")
        r1 = requests.get("http://127.0.0.1:8000/posts/3")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r1.status_code,200)
        self.assertEqual(r1.json(),[["esse foi o ultimo","ultimo q eu fiz","bla"],["teste","@rafa #canario","z"]])

    def test_l_like_post(self):
        r = requests.post("http://127.0.0.1:8000/like/1,1?likeOrDeslike=1&ativo=1")
        self.assertEqual(r.status_code,200)
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT usr_id, post_id, gostou, ativo FROM Gosta_post WHERE usr_id=1 AND post_id=1''')
            self.assertEqual(cursor.fetchone(),(1, 1, 1, 1))
            cursor.execute('''COMMIT''')

    def test_m_deslike_post(self):
        r = requests.post("http://127.0.0.1:8000/like/1,2?likeOrDeslike=0&ativo=1")
        self.assertEqual(r.status_code,200)
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT usr_id, post_id, gostou, ativo FROM Gosta_post WHERE usr_id=1 AND post_id=2''')
            self.assertEqual(cursor.fetchone(),(1, 2, 0, 1))
            cursor.execute('''COMMIT''')
        
    def test_n_desativa_like_deslike_post(self):
        r = requests.post("http://127.0.0.1:8000/unlike/1,1?ativo=0")
        self.assertEqual(r.status_code,200)
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT usr_id, post_id, ativo FROM Gosta_post WHERE usr_id=1 AND post_id=1''')
            self.assertEqual(cursor.fetchone(),(1, 1, 0))
            cursor.execute('''COMMIT''')




if __name__ == '__main__':
    unittest.main()
