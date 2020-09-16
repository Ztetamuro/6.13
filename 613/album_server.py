import album as db

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

@route("/albums/<artist>")
def show_albums(artist):
    albums = db.find_albums(artist)
    albums_count = db.album_counter(artist)
    if albums_count < 1:
        message = ("Исполнитель не найден в базе данных.")
        response = HTTPError(404, message)
    else:
        response = "{0}:\nАльбомов в базе данных - {1}.\nСписок альбомов:\n{2}".format(artist, albums_count, ",\n".join(albums))

    return response

@route("/albums", method = "POST")
def new_album():
    album = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    if album["album"] in db.find_albums(album["artist"]):
        message = "Альбом с таким названием уже имеется в базе."
        response = HTTPError(409, message)
    else:
        if not db.data_stack_valid(album):
            message = "Не все требуемые данные были введены."
            response = HTTPError(449, message)
        elif not db.year_valid(album["year"]):
            message = "Указанное значение не может быть годом."
            response = HTTPError(400, message)
        else:
            new_album = db.add_album(album)
            db.save_album(new_album)
            response = "Альбом успешно сохранен."

    return response

if __name__ == "__main__":
    run(host = "localhost", port = 8080, debug = True)