#  подключение к базе данных и создание сессии для работы с ней

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

# некоторая абстрактная декларативная база, в которую позднее будем наследовать все модели
SqlAlchemyBase = dec.declarative_base()

# получение сессий подключения к базе данных
__factory = None


def global_init(db_file):
    # на вход адрес базы данных
    global __factory
    # не существует ли уже база
    if __factory:
        return
    #  непустой адрес базы данных
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
