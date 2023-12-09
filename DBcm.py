# DataBase context manager
from typing import Optional

from pymysql import connect
from pymysql.cursors import Cursor
from pymysql.err import OperationalError


class DBContextManager:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None  # Объект подключения
        self.cursor = None  # Сам курсор

    def __enter__(self) -> Optional[Cursor]:
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            self.conn.begin()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Неверный логин или пароль.')
            elif err.args == 1049:
                print('Неверное имя базы данных')
            else:
                print(err)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type)
            print(exc_val.args)
        if self.conn and self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True
