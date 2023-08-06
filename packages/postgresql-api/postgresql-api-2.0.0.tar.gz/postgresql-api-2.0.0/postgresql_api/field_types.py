"""

Типы данных, которые можно хранить в базе данных.

"""

from __future__ import annotations

from ast import literal_eval


class FieldType:
    """
    Инструмент для создания своих типов данных.
    """

    field_types = []  # Инициализированные типы данных.

    def __init_subclass__(cls, **kwargs):
        cls.field_types.append(cls)

    @classmethod
    def adapter(cls, obj: FieldType) -> bytes:
        """
        Функция, возвращающая строку для записи в бд.
        :param obj: Объект поля.
        """

        return str(obj).encode()

    @classmethod
    def converter(cls, obj: bytes) -> FieldType:
        """
        Функция, возвращающая объект поля.
        :param obj: Строка полученная из бд.
        """

        return cls(obj.decode("utf-8"))


class Text(FieldType, str):
    pass


class Integer(FieldType, int):
    pass


class Float(FieldType, float):
    pass


class List(FieldType, list):
    @classmethod
    def converter(cls, obj: bytes) -> List:
        return List(literal_eval(obj.decode("utf-8")))


class Dict(FieldType, dict):
    @classmethod
    def converter(cls, obj: bytes) -> Dict:
        return Dict(literal_eval(obj.decode("utf-8")))
