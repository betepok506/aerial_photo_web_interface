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


# @app.route("/home2", methods=("GET", "POST"), strict_slashes=False)
# def home2():
#     return render_template("test.html", title="Home")


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
    markers_data = [
        {"lat": 54.187558, "lng": 45.167761, "name": "Marker 1", "type": "Restaurant", "address": "123 Main St",
         "rating": 4.5,
         "reviews": 100, "workingHours": "9 AM - 6 PM", "imageUrl": "https://example.com/image1.jpg"},
        {"lat": 54.177558, "lng": 45.187761, "name": "Marker 2", "type": "Cafe", "address": "456 Oak St", "rating": 4.2,
         "reviews": 80, "workingHours": "10 AM - 7 PM", "imageUrl": "https://example.com/image2.jpg"},
    ]

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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
