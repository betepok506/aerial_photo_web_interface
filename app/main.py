from flask import (
    render_template,
    make_response,
    redirect,
    request,
    flash,
    url_for,
    session,
    jsonify
)
import os
from shapely.geometry import Polygon
from shapely import wkt
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

from flask_bcrypt import check_password_hash

from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
)
from datetime import datetime
from create_app import create_app, login_manager, bcrypt
from app.models import User
from app.forms import login_form, register_form
from app.config import settings
from app.utils import send_request
import logging
import json

logging.basicConfig(filename='error.log', level=logging.DEBUG)


def jsonfilter(value):
    return json.dumps(value)


@login_manager.unauthorized_handler
def unauthorized():
    # Перенаправление на страницу логина
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    app.logger.info(f"Запросили юзера по id: {user_id}")
    user = User.get_user_by_id(int(user_id))
    user = user.json()
    if 'created_at' not in user:
        app.logger.info('Пользователь не авторизован, перенаправление...')
        return None

    del user['created_at']
    return User(**user)


app = create_app()
login_manager.login_view = 'login'
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
app.logger.addHandler(console_handler)

app.jinja_env.filters['json'] = jsonfilter


@app.before_request
def session_handler():
    session.permanent = True
    # app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home")


@app.route("/main", methods=("GET", "POST"), strict_slashes=False)
def main():
    app.logger.info(current_user)
    return render_template("main.html", title="The Eye. Главная")


@app.route("/polygons", methods=["GET"], strict_slashes=False)
def list_polygons():
    page = request.args.get("page", type=int, default=1)
    limit = 9
    skip = (page - 1) * limit

    response = send_request(
        settings.SERVER_URL + f'/api/v1/polygon/get_polygons_to_search_for?skip={skip}&limit={limit}', 'GET')
    if not 200 <= response.status_code < 300:
        raise "Ошибка добавления события"

    response = response.json()
    items = response['polygons']
    for item in items:
        item['start_time'] = datetime.strptime(item['start_time'], "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y")
        item['end_time'] = datetime.strptime(item['end_time'], "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y")
        item['created_at'] = datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
            "%H:%M:%S %d.%m.%Y")

    polygon_count = response['counts']
    total_page = (polygon_count + (limit - 1)) // limit
    # app.logger.info(items)
    return render_template("list_polygons.html", items=items,
                           page=page,
                           total_pages=total_page,
                           title="The Eye. Список полигонов")


@app.route("/create_polygon", methods=["POST"], strict_slashes=False)
def create_polygon():
    cur_user_id = current_user.id
    # app.logger.info(f'Идентификатор текущего пользователя: {cur_user_id}')
    data = request.json
    data['owner'] = cur_user_id
    polygon_id = data['polygon_id'].strip('"')
    del data['polygon_id']
    coords = json.loads(data['footprint'])
    data['footprint'] = str(Polygon(coords[0]))
    data["start_time"] = datetime.strptime(data["start_time"], "%Y-%m-%d").isoformat()
    data["end_time"] = datetime.strptime(data["end_time"], "%Y-%m-%d").isoformat()
    data["download_to"] = datetime.strptime(data["download_to"], "%Y-%m-%d").isoformat()
    if polygon_id != 'null':
        # Редактируем запись
        data['id'] = polygon_id
        response = send_request(settings.SERVER_URL + f'/api/v1/polygon/update_polygon_to_search_for', "POST", data)
        if not 200 <= response.status_code < 300:
            app.logger.warning(f'Ошибка: {response.json()}')
            raise "Ошибка редактирования события"
    else:
        response = send_request(settings.SERVER_URL + '/api/v1/polygon/create_polygon_to_search_for', "POST", data)
        if not 200 <= response.status_code < 300:
            raise "Ошибка добавления события"

    return render_template("create_polygon.html", title="Создание полигона", polygon_id=polygon_id)


@app.route('/delete_polygon', methods=['DELETE'])
@login_required
def delete_polygon():
    polygon_id = int(
        request.args.get('polygon_id'))  # Получаем параметр 'index' из строки запроса и преобразуем в целое число

    response = send_request(settings.SERVER_URL + f'/api/v1/polygon/delete_polygon_to_search_for/{polygon_id}', "DELETE")
    if not 200 <= response.status_code < 300:
        app.logger.warning(f'Ошибка: {response.json()}')
        raise f"Ошибка удаления события. Ошибка: {response.json()}"

    app.logger.info(f'Полигон с индексом {polygon_id} успешно удалено!')
    return make_response("OK", 200)


@app.route("/polygon_creation_form", methods=["GET"], strict_slashes=False)
def polygon_creation_form():
    polygon_id = request.args.get('polygon_id')
    return render_template("create_polygon.html", title="Создание полигона", polygon_id=polygon_id)


@app.route('/get_polygon', methods=["GET"])
# @login_required
def get_polygon():
    polygon_id = request.args.get('polygon_id').strip('"')
    app.logger.info(f'Получение информации polygon с индексом {polygon_id}')
    response = send_request(settings.SERVER_URL + '/api/v1/polygon/get_polygon_to_search_for?id=' + polygon_id, "GET")
    if not 200 <= response.status_code < 300:
        app.logger.warning(f'Ошибка: {response.json()}')
        raise f"Ошибка получения события. Ошибка: {response.json()}"

    data = response.json()
    data['footprint'] = list(wkt.loads(data['footprint']).exterior.coords)
    return jsonify(**data)


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            response = User.get_user_by_login(login=form.email.data)
            if 200 < response.status_code >= 300:
                raise "value error"

            print(response.json())
            user = response.json()
            del user['created_at']

            if check_password_hash(user['password'], form.pwd.data):
                login_user(User(**user))
                return redirect(url_for('main'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
                           form=form,
                           text="Авторизация",
                           title="Авторизация",
                           btn_action="Вход"
                           )


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.pwd.data
            username = form.username.data

            response = User.add_user({
                "login": email,
                "password": bcrypt.generate_password_hash(password).decode('utf-8'),
                "username": username})

            print(response)
            if 200 < response.status_code >= 300:
                raise "value error"

            app.logger.info(f'User registered!')
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            flash(f"User already exists!.", "warning")
        except DataError:
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            flash(f"An error occured !", "danger")

    return render_template("auth.html",
                           form=form,
                           text="Регистрация",
                           title="Регистрация",
                           btn_action="Зарегистрироваться"
                           )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=settings.debug, port=os.getenv("WEB_PORT", 3000))
