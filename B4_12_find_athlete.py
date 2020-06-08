from datetime import datetime
import time
from math import fabs

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(id, session):
    find_user = session.query(User).filter(User.id == id).first()
    if find_user:
        Users = session.query(User)
        first_find = True
        for user in Users.all():
            if first_find and find_user.id != user.id:
                nearest_b = user
                nearest_h = user
                first_find = False
            if not first_find and user.id != find_user.id and fabs(datetime.strptime(user.birthdate, "%d.%m.%Y").timestamp() - datetime.strptime(find_user.birthdate, "%d.%m.%Y").timestamp()) < fabs(datetime.strptime(nearest_b.birthdate, "%d.%m.%Y").timestamp() - datetime.strptime(find_user.birthdate, "%d.%m.%Y").timestamp()):
                nearest_b = user
            if not first_find and user.id != find_user.id and fabs(user.height - find_user.height) < fabs(nearest_b.height - find_user.height):
                nearest_h = user
        
        print("Вы выбрали атлета: {} {}, дата рождения: {}, рост: {}".format(find_user.first_name, find_user.last_name, find_user.birthdate, find_user.height))
        print("Ближайший по дате рождения: {} {}, дата рождения: {}, рост: {}".format(nearest_b.first_name, nearest_b.last_name, nearest_b.birthdate, nearest_b.height))
        print("Ближайший по росту: {} {}, дата рождения: {}, рост: {}".format(nearest_h.first_name, nearest_h.last_name, nearest_h.birthdate, nearest_h.height))

    else:
        print("Пользователя с таким id нет в базе.")

def main():
    session = connect_db()
    id = input("Введи id пользователя для поиска: ")
    find(id, session)

if __name__ == "__main__":
    main()