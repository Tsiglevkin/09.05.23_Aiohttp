import json

from pydantic import BaseModel, validator, ValidationError
from typing import Optional, Type
from aiohttp import web


class CreateUser(BaseModel):

    # Прописываем типы данных для запрашиваемых полей. Поля обязательны, т.к. нет параметра Optional
    name: str
    user_pass: str

    # задаем дополнительные проверки при помощи методов и декоратора validator('model_field_name')
    @validator('name')
    def validate_name(cls, value):
        """
        Проверка на длину имени.
        :param value: str
            Проверяемое значение name.
        :return:
            Проверенное значение
        """

        if value > 100:
            raise ValueError('Name is too big. You have 100 symbols.')
        return value

    @validator('user_pass')
    def validate_password(cls, value):
        """
        Проверка на длину пароля.
        :param value: str
            Проверяемое значение name.
        :return:
            Проверенное значение.
        """

        if len(value) < 8:
            raise ValueError('password is too short')
        if len(value) > 100:
            raise ValueError('password is too big')
        return value


class UpdateUser(BaseModel):
    """Валидация данных при обновлении пользователя. Проверки на тип данных и длину значения"""

    name: Optional[str]
    user_pass: Optional[str]

    @validator('name')
    def validate_name(cls, value):
        """
        Проверка на длину имени.
        :param value: str
            Проверяемое значение name.
        :return:
            Проверенное значение
        """

        if value > 100:
            raise ValueError('Name is too big. You have 100 symbols.')
        return value

    @validator('user_pass')
    def validate_password(cls, value):
        """
        Проверка на длину пароля.
        :param value: str
            Проверяемое значение name.
        :return:
            Проверенное значение.
        """

        if len(value) < 8:
            raise ValueError('password is too short')
        if len(value) > 100:
            raise ValueError('password is too big')
        return value


class CreateAdvertisement(BaseModel):
    """Валидация данных при создании объявления."""

    header: str
    desc: Optional[str]
    owner_id: int


class UpdateAdvertisement(BaseModel):
    """Валидация данных при обновлении объявления."""

    header: str
    desc: Optional[str]


def validate(
        json_data: dict,
        model_class: Type[CreateUser] | Type[UpdateUser] | Type[CreateAdvertisement] | Type[UpdateAdvertisement],
        ):
    try:
        model_item = model_class(**json_data)
        return model_item.dict(exclude_none=True)
    except ValidationError as error:
        raise web.HTTPBadRequest(
            text=json.dumps({'error': 'some data are not validate'}),
            content_type='application/json'
        )




