import os
import random

import flask
import werkzeug.utils
import requests
import flask_login
import flask_restful
from sql.data import session, register, login, users, add_authors, add_genres, add_books, findline, books
from api.users import user_resource
from api.books import book_resource, author_resource, genre_resource

app = flask.Flask(__name__)
api = flask_restful.Api(app)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
app.config["UPLOAD_FOLDER"] = "books_files"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def error_404(_e):
    return flask.render_template("error.html", text="Увы! Страница, которую вы ищете, не существует.",
                                 e=404, file="error.css")


@app.errorhandler(500)
def error_404(_e):
    return flask.render_template("error.html", text="Упс! Что-то пошло не так...",
                                 e=500, file="error.css")


@app.errorhandler(401)
def error_404(_e):
    return flask.render_template("error.html", text="Вы забыли авторизоваться!",
                                 e=401, file="error.css")


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


@app.route("/add_genre", methods=["GET", "POST"])
@flask_login.login_required
def add_genre():
    genre_form = add_genres.GenreForm()

    if genre_form.validate_on_submit():
        data = {
            "name": genre_form.name.data
        }
        requests.post(flask.request.url_root.rstrip("/") + "/api/genres", json=data)

    return flask.render_template("add_genre.html", form=genre_form)


@app.route("/add_author", methods=["GET", "POST"])
@flask_login.login_required
def add_author():
    author_form = add_authors.AuthorForm()

    if author_form.validate_on_submit():
        data = {
            "name": author_form.name.data,
            "birthday": str(author_form.birthday.data)
        }
        requests.post(flask.request.url_root.rstrip("/") + "/api/authors", json=data)

    return flask.render_template("add_author.html", form=author_form)


@app.route("/delete_author/<int:author_id>", methods=["GET", "POST"])
@flask_login.login_required
def delete_author(author_id):
    author_resource.AuthorsResource.delete(author_id)

    return flask.redirect("/")


@app.route("/add_book", methods=["GET", "POST"])
@flask_login.login_required
def add_book():
    book_form = add_books.BookForm()
    authors = requests.get(flask.request.url_root.rstrip("/") + "/api/authors").json()["authors"]
    genres = requests.get(flask.request.url_root.rstrip("/") + "/api/genres").json()["genres"]
    book_form.authors.choices = [(author["id"], author["name"]) for author in authors]
    book_form.genres.choices = [(genre["id"], genre["name"]) for genre in genres]

    if book_form.validate_on_submit():
        file = book_form.file.data
        filename = (str(len(requests.get(flask.request.url_root.rstrip("/") + "/api/books").json()["books"])) +
                    file.filename)

        data = {
            "title": book_form.title.data,
            "year": book_form.year.data,
            "description": book_form.description.data,
            "authors": book_form.authors.data,
            "genres": book_form.genres.data,
            "file": filename
        }

        requests.post(flask.request.url_root.rstrip("/") + "/api/books", json=data)

        filename = werkzeug.utils.secure_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return flask.render_template("add_book.html", form=book_form)


@app.route("/delete_book/<int:book_id>", methods=["GET", "POST"])
@flask_login.login_required
def delete_book(book_id):
    file_path = book_resource.BooksResource.delete(book_id).json["success"]
    os.remove(str(os.path.join(app.config['UPLOAD_FOLDER'], file_path)))

    return flask.redirect("/")


@app.route("/authors")
@flask_login.login_required
def display_authors():
    displayed_authors = requests.get(flask.request.url_root.rstrip("/") + "/api/authors").json()["authors"]

    return flask.render_template("authors.html", authors=displayed_authors)


@app.route("/books")
@flask_login.login_required
def display_books():
    displayed_books = requests.get(flask.request.url_root.rstrip("/") + "/api/books").json()["books"]

    return flask.render_template("books.html", books=displayed_books)


@app.route("/book/<string:book_id>")
@flask_login.login_required
def display_book(book_id):
    book = requests.get(flask.request.url_root.rstrip("/") + "/api/book/" + book_id).json()["book"]
    authors = requests.get(flask.request.url_root.rstrip("/") + "/api/books_authors/" + book_id).json()["books-authors"]
    genres = requests.get(flask.request.url_root.rstrip("/") + "/api/books_genres/" + book_id).json()["books-genres"]

    book["authors"] = [author for author in authors]
    book["genres"] = [genre["name"] for genre in genres]

    return flask.render_template("book.html", book=book)


@app.route("/download/<string:file_path>")
@flask_login.login_required
def download(file_path):
    return flask.send_file(str(os.path.join(app.config['UPLOAD_FOLDER'], file_path)), as_attachment=True)


@app.route("/author/<string:author_id>")
@flask_login.login_required
def display_author(author_id):
    author = requests.get(flask.request.url_root.rstrip("/") + "/api/author/" + author_id).json()["author"]
    authors_books = requests.get(flask.request.url_root.rstrip("/") +
                                 "/api/authors_books/" + author_id).json()["authors-books"]

    author["books"] = [{"id": book["id"], "title": book["title"]} for book in authors_books]

    return flask.render_template("author.html", author=author)


@flask_login.login_required
def find_book(string):
    connection = session.create_session()
    found_books = connection.query(books.Book).filter((books.Book.title.like(f"%{string}%"))).all()
    found_authors = connection.query(books.Author).filter((books.Author.name.like(f"%{string}%"))).all()

    return found_books, found_authors


@app.route("/", methods=["GET", "POST"])
def index():
    find_form = findline.FindForm()

    random_books = requests.get(flask.request.url_root.rstrip("/") + "/api/books").json()["books"]
    random.shuffle(random_books)

    if find_form.validate_on_submit():
        string = find_form.string.data
        found_books, found_authors = find_book(string)

        return flask.render_template("index.html", form=find_form,
                                     query=string,
                                     books=found_books,
                                     authors=found_authors,
                                     random_books=random_books[:3])

    return flask.render_template("index.html", form=find_form,
                                 random_books=random_books[:3])


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

    api.add_resource(book_resource.GenreBooksListResource, "/api/genre_books/<int:genre_id>")
    api.add_resource(genre_resource.BooksGenresListResource, "/api/books_genres/<int:book_id>")

    app.run()


if __name__ == '__main__':
    main()
