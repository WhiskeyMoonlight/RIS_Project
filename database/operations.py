from typing import List

import DBcm
from .connection import UseDatabase


def select(db_config: dict, sql: str) -> List:
    result = []
    with UseDatabase(db_config) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

    return result


def call_procedure(db_config: dict, proc_name: str, *args):
    res = []
    with DBcm.DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        params = []
        for arg in args:
            params.append(int(arg))
        cursor.callproc(proc_name, params)
        res = cursor.fetchall()

    return res


def save_order_with_list():
    pass
