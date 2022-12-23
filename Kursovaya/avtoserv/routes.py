import datetime

from avtoserv import app
from flask import render_template, request, flash, session, redirect, url_for, abort, g

from avtoserv.admin.admin import admin
from avtoserv.bd_exe import connect_db, FDataBase

'''Верхнее меню'''
menu = [{'name': 'Главная', 'url': 'index'},{'name': 'Авторизация', 'url': 'login'},{'name': 'Регистрация', 'url': 'register'},{'name': 'Отзывы', 'url': 'poluchotz'},{'name': 'Услуги', 'url': 'uslugi'}]


@app.route('/quit')
def quit():
    session.clear();
    return render_template('index.html', title='Главная', menu=menu)

app.register_blueprint(admin,url_prefix='/admin')

bd_contact=[]
'''Главная страница'''
@app.route('/')
@app.route('/index')
def index():
    db = get_db()
    db = FDataBase(db)
    print(db.getOtz())
    return render_template('index.html', title='Главная', menu=menu ,otziv=db.getOtz())

def rec(bd, f):
    print(f['username'])
    bd.append({'username': f['username'], 'message': f['message']})

'''Профиль пользователя с добавлением данных в БД'''
@app.route('/profile/<username>' , methods=["POST", "GET"] )
def profile(username):
    db = get_db()
    db = FDataBase(db)
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    if request.method == "POST" :
        print(db.getUsl())
        if len(request.form['fio']) > 2:
            flash('Заказ передан консультанту, с вами свяжутся в ближайшее время', category='success')
            db.add_uslug(request.form['fio'], request.form['contact'], request.form['usluga1'], request.form['usluga2'], request.form['usluga3'])
        else:
            flash('Ошибка отправки', category='error')
    return render_template('profile.html', title='Профиль', uslugi=db.getUsl())

'''Страница отправления отзывов, запись в БД + флеш'''
@app.route('/otzivi' , methods=["POST", "GET"] )
def otzivi():
    db = get_db()
    db = FDataBase(db)
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
            db.add_otziv(request.form['username'], request.form['email'], request.form['messeng'])
        else:
            flash('Ошибка отправки', category='error')
    return render_template('otzivi.html', title='Отзывы', menu=menu)

def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'link_db'):
        g.link_db.close()
''' страница Регистрация пользователя'''
@app.route('/register', methods=['POST', 'GET'])
def reg():
    db = get_db()
    db = FDataBase(db)
    if request.method == "POST":
        db.add_users(request.form['login'],request.form['password'])
    return  render_template('reg.html', title='Регистрация', menu=menu)


'''Страница авторизации пользователя с чтением из БД'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    db = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST':
        for item in db.getUser():
            if item['login'] == request.form['login'] and item['password'] == request.form['password']:
                session['userlogged'] = request.form['login']
                username = session['userlogged']
                print(username)
                return redirect(url_for('profile', username = username))
        else:
            print('Ошибка')
    return render_template('login.html', title='Авторизация', menu=menu, data=db.getUser())



'''Страница просмотра отзывов, чтение и вывод из БД'''
@app.route('/poluchotz')
def poluchotz():
    db = get_db()
    db = FDataBase(db)
    print(db.getOtz())
    return render_template('poluchotz.html',title = 'Отзывы', menu=menu, otziv=db.getOtz())

'''Страница просмотра услуг'''
@app.route('/uslugi')
def uslugi():
    db = get_db()
    db = FDataBase(db)
    print(db.getUsl())
    return render_template('uslugi.html', title='Услуги', menu=menu, uslugi=db.getUsl())



@app.route('/avtor')
def avtor():
    return render_template('avtor.html', title='Автор', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Все сломалось', menu=menu)

@app.errorhandler(401)
def page_error_401(error):
    return render_template('page401.html', title='Ошибка авторизации', menu=menu)

@app.route('/vixod')
def vixod():
    session.clear();
    return render_template('login.html', title='Автор', menu=menu)


@app.route('/pr')
def pr():
    return render_template('probnic.html',title = 'Отзывы', menu=menu )
