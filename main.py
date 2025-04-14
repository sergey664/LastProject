import flask
import requests
import flask_login
import flask_restful
from sql.data import session, register, login, users
from api.users import user_resource
from api.books import book_resource, author_resource, genre_resource

app = flask.Flask(__name__)
api = flask_restful.Api(app)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    connection = session.create_session()
    return connection.get(users.User, user_id)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    register_form = register.RegisterForm()

    if register_form.validate_on_submit():
        if register_form.password.data == register_form.password_repeat.data:
            data = {
                "nickname": register_form.nickname.data,
                "email": register_form.email.data,
                "password": register_form.password.data,
                "is_admin": 0
            }
            requests.post(flask.request.url_root.rstrip("/") + "/api/users", json=data)

            return flask.redirect("/login")

    return flask.render_template("register.html", form=register_form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    login_form = login.LoginForm()

    if login_form.validate_on_submit():
        connection = session.create_session()
        user = connection.query(users.User).filter((users.User.email == login_form.email.data)).first()

        if user and user.check_password(login_form.password.data):
            flask_login.login_user(user)
            return flask.redirect("/")
        return flask.render_template("login.html", message="Неправильный логин или пароль", form=login_form)

    return flask.render_template("login.html", form=login_form)


@app.route("/logout")
@flask_login.login_required
def logout_user():
    flask_login.logout_user()
    return flask.redirect("/")


@app.route("/")
def index():
    return flask.render_template("index.html")


def main():
    session.global_init("sql/db/bookery.db")

    api.add_resource(user_resource.UsersListResource, "/api/users")
    api.add_resource(user_resource.UsersResource, "/api/user/<int:user_id>")

    api.add_resource(genre_resource.GenresListResource, "/api/genres")
    api.add_resource(genre_resource.GenresResource, "/api/genre/<int:genre_id>")

    api.add_resource(author_resource.AuthorsListResource, "/api/authors")
    api.add_resource(author_resource.AuthorsResource, "/api/author/<int:author_id>")

    api.add_resource(book_resource.BooksListResource, "/api/books")
    api.add_resource(book_resource.BooksResource, "/api/book/<int:book_id>")

    api.add_resource(book_resource.AuthorsBooksListResource, "/api/authors_books/<int:author_id>")
    api.add_resource(author_resource.BooksAuthorsListResource, "/api/books_authors/<int:book_id>")

    app.run()


if __name__ == '__main__':
    main()
