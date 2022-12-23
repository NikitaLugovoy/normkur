import math
import sqlite3
from avtoserv import app
import  time


menu = [{'name': 'Главная', 'url': 'index'}, {'name': 'Блюда', 'url': 'dishes'}, {'name': 'Помощь', 'url': 'help'},
        {'name': 'Контакт', 'url': 'contact'}, {'name': 'Авторизация', 'url': 'login'},{'name':'Регистрация','url':'reg'}]

bd_userdata=[{'username':'test','psw':'test'},{'username':'root','psw':'pass'},{'username':'log','psw':'psw'}]

posts=[{'title':'test','post_message':'test'},{'title':'Что то о постах','post_message':'пост'},{'title':'Чек пост','post_message':'Чеееек'}]

def connect_db():
    '''создание соединения с бд'''
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    '''Вспомогательная функция для создания таблицы'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FDataBase:
    def __init__(self, db1):
        self.__db = db1
        self.__cursor = db1.cursor()

    def add_menu(self, usluga, zena):
        try:
            self.__cursor.execute("insert into otziv values(NULL, ?, ?)", (usluga, zena))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД" + str(e))
            return False
        return True

    '''Добавление пользователей'''
    def add_users(self, username, psw):
        try:
            self.__cursor.execute("insert into users values(NULL, ?, ?)", (username, psw))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД" + str(e))
            return False
        return True


    def add_post(self, title, post_message):
        try:
            self.__cursor.execute("insert into post values(NULL, ?, ?)", (title, post_message))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД " + str(e))
            return False
        return True

    '''Добавление пользователей'''
    def add_otziv(self, username, email, messeng):
        try:
            self.__cursor.execute("insert into otziv values(NULL, ?, ?, ?)", (username, email, messeng))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД " + str(e))
            return False
        return True

    '''Добавление заказов'''
    def add_uslug(self, fio, contact, usluga1,usluga2,usluga3):
        try:
            self.__cursor.execute("insert into vibruslug values(NULL, ?, ?, ?, ?, ?)", (fio, contact, usluga1, usluga2, usluga3))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД " + str(e))
            return False
        return True

    def add_avtusl(self, usluga, zena):
        try:
            self.__cursor.execute("insert into uslugi values(NULL, ?, ?)", (usluga, zena))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления меню в БД " + str(e))
            return False
        return True

    '''Удаление записей из БД'''
    def del_menu(self,id=0):
        if id == 0:
            self.__cursor.execute("delete from otziv ")
            self.__db.commit()
        else:
            self.__cursor.execute(f"delete from otziv where id={id}")

    def getMenu(self):
        sql = 'SELECT * FROM mainmenu'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('Ошибка чтения бд')
        return()

    '''Просмотр БД с пользователями'''
    def getUser(self):
        sql = 'SELECT * FROM users'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('Ошибка чтения бд')

    ''''''
    def getAdmin(self):
        sql = 'SELECT * FROM admin'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('Ошибка чтения бд')

    def getUserById(self, id):
        sql = 'SELECT id FROM users WHERE id = ?'
        try:
            self.__cursor.execute(sql,id)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('Ошибка чтения бд')


    def getPosts(self):
        sql = 'SELECT * FROM post'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('шибка чтения бд')
        return ()

    '''Просмотр БД с отзывами'''
    def getOtz(self):
        sql = 'SELECT * FROM otziv'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('шибка чтения бд')
        return ()

    '''Просмотре бд с услугами'''
    def getUsl(self):
        sql = 'SELECT * FROM uslugi'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('шибка чтения бд')
        return ()


    def getZakaz(self):
        sql = 'SELECT * FROM vibruslug'
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res;
        except:
            print('шибка чтения бд')
        return ()


    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cursor.execute("insert into posts values(NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))
            return False
        return True

    def deuUserById(self, id):
        if id == 0:
            self.__cursor.execute("delete from users ")
            self.__db.commit()
        else:
            self.__cursor.execute(f"delete from users where id={id}")
            self.__db.commit()

    def delZakaz(self, id):
        if id == 0:
            self.__cursor.execute("delete from vibrusl ")
            self.__db.commit()
        else:
            self.__cursor.execute(f"delete from vibrusl where id={id}")
            self.__db.commit()


if __name__ == "__main__":
    db = connect_db()
    db = FDataBase(db)
    create_db()
    print(db)
