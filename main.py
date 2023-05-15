from aiohttp import web
from function import orm_context, session_middleware

app = web.Application()  # создаем экземпляр aiohttp приложения.

# для работы нам нужен контекст, чтобы подключиться к БД, провести миграции и по окончании разорвать соединение.
app.cleanup_ctx.append(orm_context)  # регистрируем контекст в приложении, чтобы оно его видело.

# Для открытия и закрытия сессии при выполнении методов get, post и т.д. используем созданную функцию session_middleware
# добавим ее в список middleware нашего приложения.
app.middlewares.append(session_middleware)

# запускаем приложение.
web.run_app(app)
