from os import listdir, path
import json
from database.Connection import Connection
import sqlite3

def get_table_list(table_dir: str) -> list:
    table_dir_files = listdir(table_dir)
    sql_tables = []
    for file in table_dir_files:
        if file.endswith('.json'):
            pydantic_created = path.isfile(f'table_models/{file[:-5].capitalize()}.py')
            if not pydantic_created:
                sql_tables.append(file[:-5])
    return sql_tables

def get_table_json(table_dir, table_name: str):
    with open(f'{table_dir}/{table_name}.json') as f:
        table_json = json.load(f)
    return table_json

def generate_create_table_sql(table: dict) -> str:
    table_name = table['table_name']
    column_sql = []
    for column_name, column_value in table.items():
        if column_name == 'table_name':
            table_name = column_value
        else:
            column_sql.append(column_name + ' ' + column_value)
    column_sql_stmt = ', \n'.join(map(str, column_sql))
    return f'create table if not exists {table_name} (\n{column_sql_stmt}\n)'

def create_tables(table_dir: str):
    tables = get_table_list(table_dir)
    if tables.__len__() == 0: return 'no tables to create'
    connect = Connection(connect=sqlite3.connect)
    for table_name in tables:
        print(f'Creating table {table_name} . . .')
        table_json = get_table_json(table_dir, table_name)
        sql_stmt = generate_create_table_sql(table_json)
        connect.execute(sql_stmt)
        generate_pydantic_model(table_dir, table_name)
    return 'tables created'

def generate_pydantic_model(table_dir: str, table_name: str):
    print(f'Generating pydantic model for {table_name} . . .')
    table = get_table_json(table_dir, table_name)
    pydantic_lines = []
    data_type = ''
    for key, value in table.items():
        if key != 'table_name':
            if key[-3:] == '_id':
                data_type = 'Optional[int]'
            elif value[:3] == 'int':
                data_type = 'int'
            elif value[0:3] == 'dat':
                data_type = 'datetime'
            else:
                data_type = 'str'
            pydantic_lines.append(f'    {key}: {data_type}\n')
    pydantic_model = f'from pydantic import BaseModel\nfrom typing import Optional\n\nclass {table_name.capitalize()}(BaseModel):\n'
    with open(f'table_models/{table_name.capitalize()}.py', 'w') as f:
        f.writelines(pydantic_model)
        f.writelines(pydantic_lines)


if __name__=='__main__':
    print(create_tables(table_dir=f'{path.curdir}/tables_json'))