import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key = True, autoincrement = True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def db_conn():
    """
    Создает новое подключениу/сессию.
    """
    engin = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engin)
    session = sessionmaker(engin)

    return session()

def data_stack_valid(dict):
    """
    Принимает на вход словарь и проверяет наличие всех требующихся ключей. В удовлетворительном случает возвращает True,
    иначе False.
    """
    if dict["year"] and dict["artist"] and dict["genre"] and dict["album"]:
        return True
    else:
        return False

def year_valid(str):
    """
    Принимает на вход строку и проверяет является ли эта срока годом, при положительном ответе возвращает True, при
    отрицательном False.
    """
    if len(str) == 4 and str.isdigit():
        if int(str) > 1650 and int(str) < 2020:
            return True
        else:
            return False
    else:
        return False

def find_albums(artist):
    """
    Принимает на вход строчное (str) название группы и возвращает список альбомов, написанных этой группой.
    """
    session = db_conn()
    artist_target = session.query(Album).filter(Album.artist == artist).all()
    list_of_album = [album.album for album in artist_target]

    return list_of_album

def album_counter(artist):
    """
    Принимает на вход строчное (str) название группы и возвращает общее кол-во альбомов этой группы.
    """
    session = db_conn()
    num_of_album = session.query(Album).filter(Album.artist == artist).count()

    return num_of_album

def add_album(dict):
    """
    Принимает на входи словарь с данными и на основе этого словаря создает новый объект класса Album.
    """
    album = Album(
        year = dict["year"],
        artist = dict["artist"],
        genre = dict["genre"],
        album = dict["album"]
    )

    return album

def save_album(obj):
    """
    Принимает на вход объект класса Album и сохраняет данные в SQLite базу данных.
    """
    session = db_conn()
    session.add(obj)
    session.commit()
