# Импорты ниже требуются для создания моделей и работой с БД

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # импорт фабрики асинхронных движков и сессий.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy as sq


from dotenv import dotenv_values
secrets_values = dotenv_values('.env')

###

USER = secrets_values['USER']
PASSWORD = secrets_values['PASSWORD']
HOST = secrets_values['HOST']
PORT = secrets_values['PORT']
DB_NAME = secrets_values['DB_NAME']

DSN = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

engine = create_async_engine(DSN)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

###


async def orm_context(some_app):
    """
    Функция принимает экземпляр класса приложения, подключается к БД, делает миграции,
    по окончании работы закрывает соединение.
    Все, что до слова yield, выполнится на старте работы приложения. Что после - в конце работы приложения.

    :param some_app: web.Application
        экземпляр приложения.
    :return:
        None
    """

    print('START')
    async with engine.begin() as connection:  # создаем подключение.
        await connection.run_sync(Base.metadata.create_all)  # делаем миграции, т.е. создаем таблицы в БД.
    yield
    await engine.dispose()  # закрываем соединение.
    print('END')


@web.middleware  # обозначаем функцию как middleware.
async def session_middleware(request: web.Request, handler):
    """
    Функция для создания сессии подключения и ее закрытия после получения response.

    :param request:
        Запрос от клиента.
    :param handler:
        Метод-обработчик представления. Асинхронный метод get, post и т.д.
    :return:
        Объект response.
    """

    async with Session() as session:  # создаем сессию
        request['session'] = session  # добавляем в словарь request сессию
        response = await handler(request)  # отправляем запрос к методу представления
        return response


class User(Base):

    __tablename__ = 'owners'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(50), nullable=False, unique=True)
    user_pass = sq.Column(sq.String(100), nullable=False, unique=True)


class Advertisement(Base):

    __tablename__ = 'advertisements'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    header = sq.Column(sq.Text, nullable=False)
    desc = sq.Column(sq.Text, nullable=True)
    created_at = sq.Column(sq.DateTime, server_default=sq.func.now())
    owner_id = sq.Column(sq.Integer, sq.ForeignKey('owners.id'), nullable=False)

    owner = relationship('User', backref='advertisements')
