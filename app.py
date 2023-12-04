from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user, logout_user
import secrets
import sqlite3
import os
import config
import bcrypt

app = Flask(__name__)
app.secret_key = config.secret_key

login_manager = LoginManager(app)
login_manager.login_view = 'login'

database_path = 'database.db'


class User(UserMixin):
    def __init__(self, user_id, email, password, secret_key):
        self.id = user_id
        self.email = email
        self.password = password
        self.secret_key = secret_key


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        user = User(result[0], result[1], result[2], result[3])
        conn.close()
        return user

    conn.close()
    return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        result = cursor.fetchone()

        

        if result:
            # User with the same email already exists
            conn.close()
            return render_template('error.html', error_txt='Уже есть аккаунт с такой же почтой')

        secret_key = secrets.token_hex(16)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO user (email, password, secret_key) VALUES (?, ?, ?)",
                       (email, hashed_password, secret_key))

        conn.commit()
        conn.close()
        return redirect('/login.html')
    else:
        return render_template('signup.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        result = cursor.fetchone()

        conn.close()

        if result:
            hashed_password = result[2]

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                secret_key = result[3]

                conn = sqlite3.connect(database_path)
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM table_data WHERE secret_key = ?", (secret_key,))
                exist_table_data = cursor.fetchone()

                if not exist_table_data:
                    cursor.execute("INSERT INTO table_data (secret_key, title, data_json) VALUES (?, ?, '')",
                                   (secret_key, "Название Таблицы"))

                    conn.commit()

                user = User(result[0], result[1], result[2], result[3])
                conn.close()
                login_user(user)
                return redirect('/main_page.html')

        return render_template('error.html', error_txt='Неправильно введенные данные')
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login.html')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return render_template('error.html', error_txt='Пожалуйста, войдите в аккаунт')


@app.route('/main_page.html')
@login_required
def secured():
    user_id = current_user.id
    email = current_user.email
    secret_key = current_user.secret_key

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM table_data WHERE secret_key = ?", (secret_key,))
    table_data = cursor.fetchone()
    print(table_data[2])

    conn.close()

    print('<', table_data, '>')

    return render_template('main_page.html', user_id=user_id, email=email, secret_key=secret_key, table_data=table_data)


@app.route('/save_table_data', methods=['GET', 'POST'])
@login_required
def save_table_data():
    user_id = current_user.id
    secret_key = current_user.secret_key

    # Get the table data from the request
    table_data = request.json['table_html']

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("UPDATE table_data SET data_json = ? WHERE secret_key = ?", (table_data, secret_key))

    conn.commit()
    conn.close()

    return render_template('main_page.html')


@app.route('/save_table_title', methods=['POST'])
def save_table_title():
    user_id = current_user.id
    secret_key = current_user.secret_key

    title = request.json['title']

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("UPDATE table_data SET title = ? WHERE secret_key = ?", (title, secret_key))

    conn.commit()
    conn.close()

    return redirect('/index.html')


if __name__ == '__main__':
    if not os.path.exists(database_path):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE user
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           email TEXT NOT NULL,
                           password TEXT NOT NULL,
                           secret_key TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE table_data
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           secret_key TEXT NOT NULL,
                           title TEXT NOT NULL,
                           data_json TEXT NOT NULL)''')

        conn.commit()
        conn.close()

    app.run()
