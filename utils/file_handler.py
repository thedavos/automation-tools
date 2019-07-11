""" Module that handle a variety of functions that involves a file """
from os import path
from functools import wraps, reduce


def create_file(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        filename = kwargs['basename'] + '.' + kwargs['extension']

        with open(path.join(kwargs['dirname'], filename), 'w') as file:
            for row in result:
                file.write(row)

    return wrapper


def create_sql_clause_from_dict(dict_data, table_name):
    keys_list = list(dict_data.keys())
    values_list = list(map(convert_to_empty_string, list(dict_data.values())))

    columns = ','.join(keys_list)
    data = reduce(lambda acc, actual: acc + actual + ',\n', values_list, '')
    data_parsed = data[:-2]

    sql_clause = "INSERT INTO {} ({}) VALUES (\n{}\n); \n".format(table_name, columns, data_parsed)
    return sql_clause


def convert_to_empty_string(val):
    if val is None or val == 'None':
        return "NULL"
    elif type(val) is int:
        return "{}".format(val)
    else:
        print(val)
        return "'" + val + "'"
