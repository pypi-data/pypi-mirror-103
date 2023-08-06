from typing import Dict, Any

from psycopg2 import sql

from .api import PostgreSql
from .field_types import FieldType

# Постфиксы для выражения действий при вызове метода `filter`.
# filter(table_name, filed_no=1, filed_2_egt=5)
# Получится запрос “SELECT * FROM table_name WHERE filed != 0 AND field_2 >= 5”
OPT_MAP = {
    "gt": ">",
    "lt": "<",
    "no": "!=",
    "egt": ">=",
    "elt": "<=",
}


class PostgreSqlApiError(Exception):
    """ Ошибки, которые возникают при работе API """


class API(PostgreSql):
    def __init__(self, db_host: str = None):
        self._active = False

        if db_host:
            PostgreSql.__init__(self, db_host)
            self._active = True

    def save(self, *table_classes) -> str:
        """
        Функция, сохраняющая все изменения.
        :param table_classes: Объекты классов таблиц.
        :type table_classes: Table.
        :return: "Successfully"
        """

        self._check_active()

        if len(table_classes) == 0:
            raise PostgreSqlApiError("Не переданы классы таблиц")

        for obj in table_classes:
            self.execute(
                sql.SQL("UPDATE {table_name} SET {fields} WHERE id=%s").format(
                    table_name=sql.Identifier(obj.table_name),
                    fields=sql.SQL(", ").join(
                        map(
                            lambda field: sql.SQL("{field}=%s").format(
                                field=sql.Identifier(field)
                            ),
                            obj.get_fields(),
                        )
                    ),
                ),
                *(
                    field_type.adapter(obj.__dict__[field_name])
                    for field_name, field_type in obj.get_fields().items()
                ),
                obj.id,
            )
        self.commit()

        return "Successfully"

    def filter(self, table_name: str, table_fields: Dict[str, FieldType], **where):
        """
        Функция, выбирающая данные из таблицы на основе указанных параметров.
        :param table_name: Название таблицы, с которой мы работаем.
        :param table_fields: Поля, присутствующие в таблице, и их типы данных.
        :param where: Параметры сортировки.
        """

        self._check_active()
        conditions = []
        values = []

        # Формирование параметров сортировки
        for field, value in where.items():
            opt = "="
            if (index := field.rfind("_")) > 0:
                try:
                    opt = OPT_MAP[field[index + 1 :]]
                    field = field[:index]
                except KeyError:
                    pass

            if table_fields and field not in table_fields and field != "id":
                raise PostgreSqlApiError(
                    f"Поле `{field}` не найдено в таблице `{table_name}`"
                )

            conditions.append(
                sql.SQL("{field}{opt}{value}").format(
                    field=sql.Identifier(field),
                    opt=sql.SQL(opt),
                    value=sql.Placeholder(),
                )
            )  # `<field> <opt> %s`
            values.append(
                table_fields[field].adapter(value) if field != "id" else value
            )

        # Получение данных
        if conditions:
            data = self.fetchall(
                sql.SQL("SELECT * FROM {table_name} WHERE {where}").format(
                    table_name=sql.Identifier(table_name),
                    where=sql.SQL(" and ").join(conditions),
                ),
                *values,
            )
        else:
            data = self.fetchall(
                sql.SQL("SELECT * FROM {table_name}").format(
                    table_name=sql.Identifier(table_name)
                )
            )

        return [
            (
                obj[0],
                *(
                    field_type.converter(value.tobytes())
                    for field_type, value in zip(table_fields.values(), obj[1:])
                ),
            )
            for obj in data
        ]

    def insert(self, table_name: str, **fields) -> str:
        """
        Функция, добавляющая данные в таблицу.
        :param table_name: Название таблицы, с которой мы работаем.
        :param fields: {<название поля>: <значение>, ...}.
        :return: "Successfully"
        """

        self._check_active()

        self.execute(
            sql.SQL("INSERT INTO {table_name} ({fields}) VALUES ({values})").format(
                table_name=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(map(sql.Identifier, fields.keys())),
                values=sql.SQL(", ").join(sql.Placeholder() * len(fields.keys())),
            ),
            *fields.values(),
        )

        self.commit()

        return "Successfully"

    def add_field(
        self, table_name: str, field_name: str, field_type: FieldType, start_value: Any
    ) -> str:
        """
        Функция, добавляющая поле в таблицу.
        :param table_name: Название таблицы, с которой мы работаем.
        :param field_name: Название нового поля.
        :param field_type: Тип данных.
        :param start_value: Значение нового поля.
        :return: "Successfully"
        """

        self._check_active()

        self.execute(
            sql.SQL("ALTER TABLE {table_name} ADD COLUMN {field_name} bytea").format(
                table_name=sql.Identifier(table_name),
                field_name=sql.Identifier(field_name),
            )
        )  # Добавление нового поля
        self.execute(
            sql.SQL("UPDATE {table_name} SET {field_name}=%s").format(
                table_name=sql.Identifier(table_name),
                field_name=sql.Identifier(field_name),
            ),
            field_type.adapter(start_value),
        )  # Изменение стартового значения
        self.commit()

        return "Successfully"

    def create_table(self, table_name: str, **fields) -> str:
        """
        Функция, создающая таблицу в базе данных.
        :param table_name: Название таблицы.
        :param fields: {<название поля>: <тип данных>, ...}
        :return: "Successfully"
        """

        self._check_active()

        fields = [
            sql.SQL("{field} bytea").format(field=sql.Identifier(field))
            for field in fields
            if not field.startswith("_")
        ]

        self.execute(
            sql.SQL(
                "CREATE TABLE {table_name} (id SERIAL PRIMARY KEY NOT NULL, {fields})"
            ).format(
                table_name=sql.Identifier(table_name), fields=sql.SQL(", ").join(fields)
            )
        )
        self.commit()

        return "Successfully"

    def _check_active(self):
        if not self._active:
            raise PostgreSqlApiError("База данных не инициализирована")

    @property
    def cursor(self):
        """ PostgreSql cursor. """

    @cursor.getter
    def cursor(self):
        """ Получение курсора. """

        self._check_active()
        return self._cursor

    def __del__(self):
        if self._active:
            self.close()
