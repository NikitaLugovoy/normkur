from flask import Blueprint, render_template, request, url_for, redirect, session, g, flash

admin = Blueprint('admin', __name__ , template_folder='templates', static_folder='static')

from avtoserv.bd_exe import connect_db, FDataBase

 
def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db



def login_admin():
    session['admin_logged'] = 1

def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/adminprof/<username>' , methods=["POST", "GET"] )
def adminprof(username):

    return render_template('admin/adminprof.html', title='Профиль')


@admin.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    db = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('.adminprof', username=session['userlogged']))
    elif request.method == 'POST':
        for item in db.getAdmin():
            if item['login'] == request.form['login'] and item['password'] == request.form['password']:
                session['userlogged'] = request.form['login']
                username = session['userlogged']
                print(username)
                return redirect(url_for('.adminprof', username=username))
        else:
            print('Ошибка')
    return render_template('admin/login.html', title='ДляАдминистратора' , data=db.getAdmin())

@admin.route('/logout', methods=['POST', 'GET'])
def logout():

    logout_admin()

    return redirect(url_for('.login'))

@admin.route('/zakazi')
def zakazi():
    db = get_db()
    db = FDataBase(db)
    print(db.getZakaz())
    return render_template('admin/zakazi.html', title='Заказы' ,vibrusl=db.getZakaz())


@admin.route('/dobuser', methods=['POST', 'GET'])
def dobuser():
    db = get_db()
    db = FDataBase(db)
    if request.method == "POST":
        db.add_users(request.form['login'],request.form['password'])
        flash('Пользователь добавлен', category='success')
    return  render_template('admin/dobuser.html', title='ДобавлениеПользователей')

@admin.route('/dobusl' , methods=["POST", "GET"] )
def dobusl():
    db = get_db()
    db = FDataBase(db)
    if request.method == "POST":
        if len(request.form['usluga']) > 2:
            flash('Сообщение отправлено', category='success')
            db.add_avtusl(request.form['usluga'], request.form['zena'])
        else:
            flash('Ошибка отправки', category='error')
    return render_template('admin/dobusl.html', title='ДобавлениеУслуги')


@admin.route('/delusers')
def delusers():
    db = get_db()
    db = FDataBase(db)
    users = db.getUser()
    return render_template('admin/delusers.html', title='Удалить пост',users=users)


@admin.route('/delusers/<num>')
def deluser(num):
    db = get_db()
    db = FDataBase(db)
    try:
        db.deuUserById(num)
        return redirect(url_for('.delusers'))
    except:
        return 'error'

@admin.route('/vixod')
def vixod():
    session.clear();
    return render_template('login.html', title='Автор')
