from aiohttp import web
from models import User, Advertisement
from function import get_orm_item, hash_password
from schema import validate


class UserView(web.View):

    async def get(self):
        """
        Метод get возвращает данные конкретного пользователя.

        :return: dict
            json с данными пользователя
        """

        # сессия хранится в объекте (request['session']), помещена туда при помощи session_middleware.
        user_id = int(self.request.match_info.get('user_id'))  # ! проверить правильность имени поля id
        user = await get_orm_item(User, user_id, session=self.request.get('session'))  # получаем пользователя
        response = web.json_response({'user_id': user.id, 'user_name': user.name})  # json с данными пользователя
        return response

    async def post(self):
        """
        Метод POST позволяет создать пользователя и вернуть json с его id.

        :return: dict
            Json с id пользователя.
        """

        user_data = await self.request.json()  # принятые данные из request
        validated_data = validate(json_data=user_data, model_class=User)  # валидируем данные при помощи написанной ф-и.
        user_password = validated_data.get('password')  # достаем пароль
        hashed_pass = hash_password(user_password)  # хэшируем его.
        validated_data['password'] = hashed_pass  # вставляем обратно в валидированные данные.
        new_user = User(**validated_data)  # создаем нового пользователя
        self.request.get('session').add(new_user)  # Добавляем в сессии. Сессия находится в request['session']
        await self.request.get('session').commit()  # делаем коммит.
        return web.json_response({'user_id': new_user.id})  # возвращаем json с данными пользователя.

    async def patch(self):
        """
        Метод PATCH позволяет обновить данные пользователя. Если есть пароль, то метод проведет хэширование.

        :return: dict
            json словарь с id пользователя, чьи данные изменены.
        """

        user_id = int(self.request.match_info.get('user_id'))  # достаем id пользователя.
        json_data = await self.request.json()  # получаем данные из запроса
        validated_data = validate(json_data=json_data, model_class=User)  # валидируем данные
        if 'password' in validated_data:  # если есть пароль в данных, хэшируем его
            validated_data['password'] = hash_password(validated_data.get('password'))

        # получаем пользователя из БД
        user = await get_orm_item(item_class=User, item_id=user_id, session=self.request['session'])
        for field, value in validated_data.items():  # устанавливаем валидные значения пользователю.
            setattr(user, field, value)
        self.request['session'].add(user)  # добавляем данные в БД
        await self.request['session'].commit()  # делаем коммит

        return web.json_response({'user_id': user_id})  # возвращаем json с id.

    async def delete(self):
        """
        Метод DELETE удаляет пользователя, id которого переданно в запросе.

        :return: dict
            json словарь со статусом.
        """

        user_id = int(self.request.match_info.get('user_id'))  # достаем id пользователя.
        user = await get_orm_item(item_class=User, item_id=user_id, session=self.request['session'])
        session = self.request['session']
        await session.delete(user)
        await session.commit()
        return web.json_response({'status': 'deleted'})


class AdvertisementView(web.View):

    async def get(self):
        pass

    async def post(self):
        pass

    async def patch(self):
        pass

    async def delete(self):
        pass
