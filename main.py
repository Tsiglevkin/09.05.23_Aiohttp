from aiohttp import web
from function import orm_context, session_middleware
from views import UserView, AdvertisementView

app = web.Application()  # создаем экземпляр aiohttp приложения.

# для работы нам нужен контекст, чтобы подключиться к БД, провести миграции и по окончании разорвать соединение.
app.cleanup_ctx.append(orm_context)  # регистрируем контекст в приложении, чтобы оно его видело.

# Для открытия и закрытия сессии при выполнении методов get, post и т.д. используем созданную функцию session_middleware
# добавим ее в список middleware нашего приложения.
app.middlewares.append(session_middleware)

# прописываем роуты
app.add_routes(
    [
        web.post('/users/', UserView),
        web.get('/users/{user_id:\d+}', UserView),
        web.patch('/users/{user_id:\d+}', UserView),
        web.delete('/users/{user_id:\d+}', UserView),
    ]
)

# запускаем приложение.
web.run_app(app)
