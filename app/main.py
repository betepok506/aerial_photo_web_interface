from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    url_for,
    session,
    jsonify
)
import os

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from models import User
from forms import login_form, register_form

markers_data = [
    {"lat": 54.191127, "lng": 45.177953, "idx": 1, "name": "Профком", "type": "Кальян-бар",
     "address": "Пролетарская ул., 81",
     "rating": 4.5,
     "reviews": 33,
     "workingHours": "17:00 - 01:00",
     "imagesUrl": ["https://avatars.mds.yandex.net/get-altay/9368060/2a0000018944034872a9c0dbe175d5be9576/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/10829645/2a0000018aae6594924d4f66b7992b90fb0d/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/9691438/2a0000018aae6354db409471f29c8bfa9181/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/10147638/2a0000018a3ca98dd4d394d45a04f1e46fa6/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/6548191/2a0000018a3caa33df0dcd975762eae38d07/XXXL"
                   ],
     "description": "Отличное место, можно отдохнуть как в одиночестве, так и в компании. Уютная, спокойная и расслабляющая атмосфера. Кальяны на высшем уровне, идеальная крепость, отменно, дымно, вкусно:)"},

    {"lat": 54.186961, "lng": 45.175325, "idx": 2, "name": "Солнце и Луна", "type": "Ресторан",
     "address": "ул. Богдана Хмельницкого, 40", "rating": 4.4,
     "reviews": 97,
     "workingHours": "10:00 - 00:00",
     "imagesUrl": ["https://avatars.mds.yandex.net/get-altay/1779701/2a00000184cd61b6dff977f177bdb42ef678/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/1871297/2a00000184cd614db5cdad3db541fda65590/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/7810332/2a00000184cd5fe88f450dbb819178bc8f0d/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/788991/2a00000184cd5fa9cceeb561a9f45b499ffa/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/5584339/2a0000017d93862d392c8383c048ea6d9de5/XXXL"],
     "description": "Уютная атмосфера , красивый интерьер, еда всегда очень вкусная - повара стараются ,выбор блюд огромен можно провести как банкет так и просто прийти поужинать."},

    {"lat": 54.186533, "lng": 45.177716, "idx": 3, "name": "Мао", "type": "Ресторан", "address": "Пролетарская ул., 43",
     "rating": 4.4,
     "reviews": 125,
     "workingHours": "10:00 - 23:00",
     "imagesUrl": ["https://avatars.mds.yandex.net/get-altay/5482460/2a0000017e3d4c55bf78978f6ea8dfbbe3f5/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/1045589/2a000001873e149c8240e9334a1ca4a294a7/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/6527792/2a000001880be23ef021a274076d7f7f9302/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/8072647/2a00000184f22b30c5c48bcb56d5acb25625/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/5598654/2a0000017cbf4a0cba1f4e56cddb93f0049c/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/771751/2a000001880be23f08f4a548ec19f22f41cd/XXXL"],
     "description": "В ресторане Mao можно попробовать паназиатские блюда, такие как суп «Рамен», запеченные роллы, жареное молоко и другие. Кроме того, посетители высоко оценивают уютную атмосферу и приятную музыку в ресторане."},

    {"lat": 54.185953, "lng": 45.187322, "idx": 4, "name": "Милано", "type": "Пиццерия",
     "address": "просп. Ленина, 10Б", "rating": 4.3,
     "reviews": 213,
     "workingHours": "10:00 - 22:05",
     "imagesUrl": ["https://avatars.mds.yandex.net/get-altay/9368060/2a0000018991f5fcd0a1a48549f5a24108c3/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/938969/2a0000018907ca0ee235356374fd43e07f23/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/4437253/2a00000178f21ab8467071ffd115f3ab842e/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/3935166/2a000001884efa1265c9a99952a429f87973/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/4504251/2a0000017835884615678fafbe1bad18f4ea/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/4012648/2a00000178358b9abaa4f71c4fe214ca92a3/XXXL"],
     "description": "Очень вкусная пицца, большой выбор, на любой вкус. Находятся в самом центре, удобно зайти и быстро перекусить. Есть доставка"},

{"lat": 54.183046, "lng": 45.182249, "idx": 5, "name": "Та самая", "type": "Кондитерская",
     "address": "Большевистская ул., 13", "rating": 4.4,
     "reviews": 87,
     "workingHours": "07:00 - 23:00",
     "imagesUrl": ["https://avatars.mds.yandex.net/get-altay/750770/2a0000018581ea209145cde6a5146c0da770/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/5253303/2a0000017c0599ab543b35ffdb8a3288cdf1/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/4587805/2a00000177d82b72d6d1623c206d6c7710ad/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/4441482/2a00000177d82b0d788ed0273afbb38ac20e/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/4618902/2a00000178f57fb01b69a7c783a4f404ef84/XXXL",
                   "https://avatars.mds.yandex.net/get-altay/9284964/2a00000189f06c3e2a2abf2adcf5055bca4a/XXXL"],
     "description": "Хорошая кондитерская с большим выбором выпечки и разных, разностей. Приятный персонал и удобное месторасположение кафе."}
]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    # app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home")


@app.route("/main", methods=("GET", "POST"), strict_slashes=False)
def main():
    return render_template("main.html", title="Way To Rest")


@app.route("/events", methods=("GET", "POST"), strict_slashes=False)
def events():
    return render_template("events.html", title="События")


@app.route("/create_event", methods=("GET", "POST"), strict_slashes=False)
def create_event():
    return render_template("create_event.html", title="Создание события")


@app.route("/about", methods=("GET", "POST"), strict_slashes=False)
def about():
    return render_template("about.html", title="О нас")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('main'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
                           form=form,
                           text="Login",
                           title="Login",
                           btn_action="Login"
                           )


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )

            db.session.add(newuser)
            db.session.commit()
            app.logger.info(f'User registered!')
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")

    return render_template("auth.html",
                           form=form,
                           text="Create account",
                           title="Register",
                           btn_action="Register account"
                           )


@app.route("/getMarkers/", methods=["GET"])
def getMarkers():
    # 54.187558, 45.177761

    ne_lat = float(request.args.get('neLat'))
    ne_lng = float(request.args.get('neLng'))
    sw_lat = float(request.args.get('swLat'))
    sw_lng = float(request.args.get('swLng'))
    print(f"{ne_lat} {ne_lng} {sw_lat} {sw_lng}")

    # Пример логики фильтрации маркеров в пределах границ
    filtered_markers = [
        marker for marker in markers_data
        if sw_lat <= marker['lat'] <= ne_lat and sw_lng <= marker['lng'] <= ne_lng
    ]

    return jsonify(filtered_markers)


@app.route("/get_marker_by_idx/", methods=["GET"])
def get_marker_by_idx():
    idx = float(request.args.get('index'))
    print(f"{idx}")

    for cur_marker in markers_data:
        if cur_marker['idx'] == idx:
            return jsonify(cur_marker)

    return 1


@app.route("/landing_page/", methods=["GET"])
def landing_page():
    return render_template("landing_page.html", title="Лендинг")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.getenv("WEB_PORT", 8000))
