from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
import sqlite3
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
menu = [{'url': '.index', 'title': 'Панель'}, {'url': '.logout', 'title': 'Выйти'}]

db = None


@admin.before_request
def before_request():
    """Подключение к базе"""
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route("/")
@admin.route("/index")
def index():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей - admin.index")

    return render_template("admin/index.html", title="Главная", menu=menu, list=list)


@admin.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['username'] == 'admin' and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль")
    return render_template("admin/login.html", title="Войти")


def login_admin():
    session["admin_logged"] = 1


def logout_admin():
    session.pop('admin_logged', None)


def isLogged():
    return True if session.get('admin_logged') else False


@admin.route("/logout")
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))
