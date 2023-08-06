"""

Всё что нужно для создания класса таблицы

"""

from __future__ import annotations

from typing import Literal, get_type_hints, Dict, Any

from .field_types import Text, Integer, Float, List, Dict, FieldType
from .main import API, PostgreSqlApiError


class Table(object):
    """ Родительский класс для создания таблиц """

    id: int = None

    def __init__(self, db_host: str = None, _api: API = None, **kwargs):
        """
        :param db_host: URL к базе данных.
        :param _api: PostgreSql Api
        """

        self.__api = _api or API(db_host)
        self.__inited = bool(_api)
        self.__dict__.update(**kwargs)

    def save(self) -> str:
        """
        Функция, сохраняющая все изменения.
        :return: "Successfully"
        """

        return self.__api.save(self)

    def update(self, **fields) -> str:
        """
        Функция, обновляющая значения полей и автоматически сохраняя изменения.
        :param fields: {<название поля>: <значение>, ...}
        :return: "Successfully"
        """

        self.__dict__.update(**fields)
        return self.save()

    def filter(
        self,
        return_type: Literal["visual", "classes"] = "classes",
        return_list: Literal[True, False] = False,
        **where,
    ):
        """
        Функция, выбирающая данные из таблицы на основе указанных параметров.
        :param return_type:
            Для "classes" - вернёт объект класса таблицы.
            Для "visual" - вернёт данные в том виде,
                в котором они хранятся в базе данных.
        :param return_list:
            Для True - вернёт список объектов независимо от их количества.
        :param where: Параметры сортировки.
        :return: Объект или список объектов классов таблицы.
        """

        if data := self.__api.filter(
            table_name=self.table_name,
            table_fields=self.get_fields(),
            **where,
        ):
            if return_type == "visual":
                if return_list:
                    return data

                return data[0] if len(data) == 1 else data

            else:
                data = [self.get_class(obj) for obj in data]
                if return_list:
                    return data

                return data[0] if len(data) == 1 else data

        return [] if return_list else None

    def insert(self, **fields) -> str:
        """
        Функция, добавляющая данные в таблицу.
        :param fields: {<название поля>: <значение>, ...}.
        :return: "Successfully"
        """

        table_fields = {
            field: vars(self.__class__).get(field)
            for field in self.get_fields()
            if vars(self.__class__).get(field) is not None
        }  # Получаем значения по умолчанию
        table_fields.update(**fields)

        if len(_fields := set(table_fields) - set(self.get_fields())):
            raise PostgreSqlApiError(
                f"В таблице `{self.table_name}` не найдены поля: "
                f'{", ".join(_fields)}'
            )

        if len(_fields := set(self.get_fields()) - set(table_fields)):
            raise PostgreSqlApiError(
                f'Не переданы значения для полей: {", ".join(_fields)}'
            )

        return self.__api.insert(
            table_name=self.table_name, **self.adapt_fields(table_fields)
        )

    def create_table(self) -> str:
        """
        Функция, создающая таблицу в базе данных.
        :return: "Successfully"
        """

        return self.__api.create_table(table_name=self.table_name, **self.get_fields())

    def add_field(self, field_name: str, start_value=None) -> str:
        """
        Функция, добавляющая поле в таблицу.
        :param field_name: Название нового поля.
        :param start_value: Значение нового поля.
        :return: "Successfully"
        """

        if not (field_type := self.get_fields().get(field_name)):
            raise PostgreSqlApiError(
                f"Поле `{field_name}` не найдено "
                f"в классе таблицы `{self.table_name}`"
            )

        if start_value is None:
            if (start_value := self.__class__.__dict__.get(field_name)) is None:
                raise PostgreSqlApiError(
                    f"Не указано значение по умолчанию для поля `{field_name}`"
                )

        return self.__api.add_field(
            table_name=self.table_name,
            field_name=field_name,
            field_type=field_type,
            start_value=start_value,
        )

    def get_class(self, data) -> Table:
        """
        Функция, возвращающая объект,
        основываясь на данных, полученных из базы данных.
        :param data: Данные об объекте.
        :return: Объект класса таблицы.
        """

        fields = dict(id=data[0], **dict(zip(self.get_fields(), data[1:])))
        return self.__class__(**fields, _api=self.__api)

    def adapt_fields(self, fields: Dict[str, Any]):
        """
        Функция, конвертирующая значения,
        для сохранения в базу данных, используя `adapter`
        """

        fields_types: Dict[str, FieldType] = self.get_fields()
        return {
            field_name: fields_types[field_name].adapter(value)
            for field_name, value in fields.items()
        }

    def convert_fields(self, fields: Dict[str, Any]):
        """
        Функция, конвертирующая значения,
        полученные из базы данных, в нужный тип данных.
        """

        fields_types: Dict[str, FieldType] = self.get_fields()
        return {
            field_name: fields_types[field_name].converter(value)
            for field_name, value in fields.items()
        }

    @classmethod
    def get_fields(cls) -> Dict[str, FieldType]:
        """ Функция, возвращающая поля и их типы данных. """

        type_map = {str: Text, int: Integer, float: Float, dict: Dict, list: List}
        fields = {}
        for field_name, field_type in get_type_hints(cls).items():
            if field_type not in type_map and field_type not in FieldType.field_types:
                raise PostgreSqlApiError(
                    f"Неподдерживаемый тип {field_type} "
                    f"у поля `{field_name}` в таблице {cls.table_name}"
                )
            field_type = type_map[field_type] if field_type in type_map else field_type
            fields[field_name] = field_type
        del fields["id"]
        return fields

    @property
    def table_name(self):
        """ Название таблицы. """

    @table_name.getter
    def table_name(self) -> str:
        """ Получение названия таблицы. """

        return type(self).__name__.lower()

    def __repr__(self):
        return "{table_name} OBJECT\n{fields}".format(
            table_name=self.table_name.upper(),
            fields="\n".join(
                f"{k}={v}" for k, v in vars(self).items() if not k.startswith("_Table_")
            ),
        )
