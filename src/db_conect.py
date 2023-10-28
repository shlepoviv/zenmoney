from pathlib import Path

import psycopg2
from psycopg2 import sql
from psycopg2.extras import register_uuid
from psycopg2.extensions import adapt, register_adapter

from src.enums import AccauntType
from src.conf_pars import read_config


def _adapt_point(class_enum):
    val = adapt(class_enum.value)
    return val

def get_data(query: str, params:dict=None):
    res = None
    with psycopg2.connect(**read_config('db')) as conn:
        with conn.cursor() as curs:
            register_uuid()
            register_adapter(AccauntType, _adapt_point)
            if not params:
                curs.execute(query)
            elif isinstance(params, dict):
                curs.execute(query, params)
            else:
                curs.executemany(query, params)
            if curs.rowcount > 0 and curs.statusmessage.startswith('SELECT'):
                res = curs.fetchall()
    return res

def create_tables() -> list:
    with open(Path('init', 'init_db_zenmoney.sql'), 'r',encoding='utf-8') as f:
        init_query = sql.SQL(f.read()).format()
    get_data(init_query)

def get_db_tables() -> list:
    responce = get_data('SELECT table_name FROM information_schema.tables\
                            WHERE table_schema=%(table_schema)s', {'table_schema': 'public'})
    if responce:
        return [row[0] for row in responce]
    return []

def get_columns_in_tabele(name_table: str) -> list:
    return [row[0] for row in (get_data('SELECT column_name \
    FROM information_schema.columns\
    WHERE table_schema = %(table_schema)s\
    AND table_name   = %(name_table)s', {'table_schema': 'public', 'name_table': name_table}))]

def get_insert_query(name_table: str, list_fields: list[str]) -> str:
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholder}) ").format(
        table=sql.Identifier(name_table),
        fields=sql.SQL(',').join(map(sql.Identifier, list_fields)),
        placeholder=sql.SQL(', ').join(map(sql.Placeholder, list_fields)))
    return query



if __name__ == '__main__':
    _t = get_db_tables()[0]
    _c = get_columns_in_tabele('serverTimestamp')
    print(_t)
    print(_c)
    print(get_insert_query(_t, _c))
    print(get_db_tables())
    print(get_data(sql.SQL('select * from {table}').format(table=sql.Identifier('zenmoneyuser'))))
    print(get_data(sql.SQL('select * from {table}').format(table=sql.Identifier('transaction'))))