from typing import Union

import psycopg2 as sql
import psycopg2.extensions
from psycopg2.sql import Composed


class PostgreSqlApiOperationalError(sql.OperationalError):
    """ Ошибки запросов. """

    def __init__(
        self,
        err: sql.OperationalError,
        request: Union[str, Composed],
        args: tuple,
        cursor: psycopg2.extensions.cursor,
    ):
        self.err_info = str(err)
        self.request = (
            request if isinstance(request, str) else request.as_string(cursor)
        )  # Запрос, который вызвал исключение
        self.args = args  # Аргументы запроса

    def __str__(self):
        return f"{self.err_info}. request: {self.request}. args: {self.args}"


class PostgreSql:
    def __init__(self, db_host):
        self._connection = sql.connect(db_host, sslmode="require")
        self._cursor = self._connection.cursor()

    def fetchall(self, request: Union[str, Composed], *args):
        """
        Функция, выполняющая запрос `request`
        и возвращающая результат используя fetchall
        """

        self.execute(request, *args)
        return self._cursor.fetchall()

    def execute(self, request: Union[str, Composed], *args):
        """ Функция, выполняющая запрос `request` """

        try:
            self._cursor.execute(request, args)
        except sql.OperationalError as err:
            raise PostgreSqlApiOperationalError(err, request, args, self._cursor)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()
