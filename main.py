from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
import base64
from io import BytesIO
from PIL import Image
from art import *
from colorama import Fore, Back, Style
from flask_cors import CORS


Art = text2art("CodeCrunch",font='big',chr_ignore=True) # console logo
print(Fore.GREEN + Art)
print(Fore.LIGHTWHITE_EX)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '9991secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
questions = []
optionsArray = []
db = SQLAlchemy(app)
first_request_initialized = False


@app.before_request
def before_request():
    global first_request_initialized
    if not first_request_initialized:
        db.create_all()
        first_request_initialized = True


class Base64Image:
    def __init__(self, base64_str, filename='default_image'):
        # Проверяем наличие заголовка в строке и обрабатываем соответствующим образом
        if ";base64," in base64_str:
            # Если в строке есть информация о MIME, разделяем ее на заголовок и данные
            header, base64_encoded_data = base64_str.split(";base64,")
            self.base64_str = base64_encoded_data
            _, extension = header.split('/')
            self.extension = extension if extension != 'jpeg' else 'jpg'
        else:
            # Если в строке нет заголовка, предполагаем, что данные в формате PNG
            self.base64_str = base64_str
            self.extension = 'png'  # Стандартное расширение, если не удается определить другое

        self.filename = filename
        self.image = self._decode()

    def _decode(self):
        # Теперь функция просто декодирует данные и загружает изображение
        decoded_data = base64.b64decode(self.base64_str)
        image = Image.open(BytesIO(decoded_data))
        return image

    def save(self, path="", filename_override=None):
        filename = filename_override if filename_override else f"{self.filename}.{self.extension}"
        full_path = f"{path}{filename}"
        self.image.save(full_path)
        return full_path
    def save(self, path="", filename_override=None):
        if filename_override:
            full_filename = filename_override
        else:
            full_filename = f"{self.filename}.{self.extension}"
        full_path = f"{path}{full_filename}"
        self.image.save(full_path)
        return full_path
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    unitytest = db.Column(db.String(100))
    pytest = db.Column(db.String(100))
    jstest = db.Column(db.String(100))

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testname = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    options = db.Column(db.String, nullable=False)
    correctAnswer = db.Column(db.String, nullable=False)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extension(filename):
    """
    Возвращает расширение файла, начиная с последней точки.

    :param filename: Имя файла с возможным расширением.
    :return: Расширение файла с точкой или пустая строка, если расширение отсутствует.
    """
    # Находим индекс последней точки в строке
    last_dot_index = filename.rfind('.')

    # Проверяем, есть ли после точки какое-либо расширение
    if last_dot_index != -1:
        # Возвращаем расширение файла
        return filename[last_dot_index:]
    else:
        # Возвращаем пустую строку, если точка не найдена
        return ""

@app.route('/admin')
def admin():
    return render_template('Admin.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        nick = request.form.get('nickname')
        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('register'))

        # Создаем нового пользователя
        new_user = User(nickname=nick,
                        email=email,
                        password=generate_password_hash(password, method='pbkdf2:sha256'),
                        unitytest=0, pytest=0, jstest=0)

        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id



        base64_string = request.form['avatarBase64']

        if not base64_string:
            return 'No image data found', 400

        # Создаем экземпляр класса Base64Image
        img = Base64Image(base64_string)

        # Проверяем, допустимо ли расширение файла.
        filename = secure_filename(img.filename + '.' + img.extension)
        if allowed_file(filename):
            # Указываем имя файла без '@' и добавляем расширение
            avatar_filename = email + get_extension(filename)
            # Сохраняем изображение в папку UPLOAD_FOLDER
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
            img.save(filename_override=save_path)  # Убедиться, что метод save принимает полный путь
            new_user.avatar = avatar_filename
        else:
            return 'File type not allowed', 400
        try:
            # Пытаемся добавить пользователя и сохранить изменения
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('profile'))
        except sqlalchemy.exc.IntegrityError:
            # Если возникла ошибка IntegrityError, то откатываем изменения
            db.session.rollback()
            return redirect(url_for('register'))

    return render_template('Register.html')


@app.route('/add_test_batch', methods=['POST'])
def add_test():
    global questions, optionsArray

    data = request.get_json()
    iteration = data['iteration']
    testName = data.get('testName')
    question = data.get('question')
    options = data.get('options')
    selectedOption = data.get('selectedOption')

    questions.append(question)
    optionsArray.extend(options)

    def combine_strings(strings_list, delimiter="|"):
        # Объединяем строки из списка, используя заданный разделитель
        combined_string = delimiter.join(strings_list)
        return combined_string
    if iteration == 2:
        # Предполагается, что у вас есть класс Test и функция для добавления в БД, которые здесь не описаны
        print(testName)
        print(combine_strings(questions))
        print(combine_strings(optionsArray))
        # new_test = Test(testname=testName,
        #                 question=combine_strings(questions),
        #                 options=combine_strings(optionsArray),
        #                 correctAnswer=selectedOption)
        # Здесь должен быть код для сохранения объекта new_test в базу данных
        # Не забываем очистить глобальные переменные после сохранения
        questions.clear()
        optionsArray.clear()

        return jsonify({"message": f"Тест '{testName}' успешно добавлен."})

    # Если iteration не равен 10, возвращаем сообщение о текущем статусе
    return jsonify({"message": f"Тест №{iteration} успешно принят, накопление данных..."})



@app.route('/')
def mainpage():
    is_authenticated = 'user_id' in session  # здесь будит True, если пользователь авторизован
    return render_template('Index.html', is_authenticated=is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))

    return render_template('Login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/process', methods=['POST'])
def process():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    user_id = session['user_id']
    data = request.get_json(force=True)

    page = data.get('page')
    variable = data.get('variable')

    if not page or variable is None:
        return jsonify({"error": "Missing 'page' or 'variable' data"}), 400

    if hasattr(User, page):
        user = db.session.get(User, user_id)
        if user:
            setattr(user, page, variable)
            db.session.commit()

            return jsonify({"success": f"Column {page} updated with value {variable} for user {user_id}."})
        else:


            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": f"Column {page} does not exist in User model"}), 400


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


def find_avatar_filename(email):
    base_dir = os.path.abspath(os.path.dirname(__file__))  # file заменено на __file__
    upload_dir = os.path.join(base_dir, 'uploads')  # убран слеш перед uploads
    # Имя файла без расширения, оставляем email без изменений
    filename_without_extension = email

    for extension in ALLOWED_EXTENSIONS:
        # Дополнительно очищаем только расширение файла, но не само имя файла
        safe_extension = secure_filename(extension)
        filename = f"{filename_without_extension}.{safe_extension}"  # Создаем имя файла
        file_path = os.path.join(upload_dir, filename)  # Полный путь к файлу
        if os.path.isfile(file_path):
            return filename

    return None  # Если файл не найден, возвращаем None


@app.route('/profile')
def profile():
    is_authenticated = 'user_id' in session
    if is_authenticated:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        if user:
            email = user.email
            utest = user.unitytest
            jtest = user.jstest
            ptest = user.pytest
            avatar_filename = find_avatar_filename(email)
            if avatar_filename:
                avatar_url = url_for('uploaded_file', filename=avatar_filename)
            else:
                avatar_url = url_for('static', filename='default-avatar.svg')  # Путь к аватару по умолчанию
            return render_template('profile.html', user=user, is_authenticated=is_authenticated, avatar_url=avatar_url, javastest=jtest,
                                   pythtest=ptest, unitygametest=utest)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/about')
def about():
    is_authenticated = 'user_id' in session  # здесь будит True, если пользователь авторизован
    return render_template('About.html', is_authenticated=is_authenticated)


@app.route('/tests')
def tests():
    is_authenticated = 'user_id' in session  # здесь будит True, если пользователь авторизован
    return render_template('Tests.html', is_authenticated=is_authenticated)

@app.route('/unitytest')
def unitytest():
    is_authenticated = 'user_id' in session  # здесь будит True, если пользователь авторизован
    return render_template('Unitytest.html', is_authenticated=is_authenticated)


@app.route('/pytest')
def pytest():
    is_authenticated = 'user_id' in session  # здесь будит True, если пользователь авторизован
    return render_template('Pytest.html', is_authenticated=is_authenticated)


@app.route('/jstest')
def jstest():
    is_authenticated = 'user_id' in session  # здесь будит True, если пользователь авторизован
    return render_template('Jstest.html', is_authenticated=is_authenticated)


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
