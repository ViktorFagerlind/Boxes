import sqlite3

from contextlib import closing
from enum import Enum
from common import boxes_pb2

'''
def ct_to_str(ct):
    if ct == boxes_pb2.ColumnType.REAL:
        return "REAL"
    if ct == boxes_pb2.ColumnType.INTEGER:
        return "INTEGER"
    if ct == boxes_pb2.ColumnType.STRING:
        return "TEXT"
    return "NULL"

def quoted(s):
    return "'" + s + "'"

def c_to_str(ct, cvs, i):
    return cvs.str_values[i] if ct == boxes_pb2.ColumnType.STRING else cvs.num_values[i]
'''

def print_db_rows(it):
    for row in it:
        print_db_row(row)

def print_db_row(row):
    for item in row:
        print('{:>23}'.format('None' if item == None else str(item)), end='')
    print('')

class Database:
    class Result(Enum):
        Success = 1
        TableMissing = 2

    # Keep the memory connection open, otherwise the database will be lost
    def __init__(self):
        try:
            self.conn = sqlite3.connect('file::memory:?cache=shared', uri=True)
            print('Connected to in-memory sqlite dB, sqlite3 version: ' + sqlite3.version)
        except Exception as e:
            print(e)


    def __del__(self):
        self.conn.close()


    def connection_decorator(func):
        def wrap_function(*args, **kwargs):
            with closing(sqlite3.connect('file::memory:?cache=shared', uri=True)) as conn:
                with closing(conn.cursor()) as c:
                    kwargs['connection'] = conn
                    kwargs['cursor'] = c
                    return func(*args, **kwargs)
        return wrap_function


    def missing_table_decorator(func):
        def wrap_function(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return Database.Result.Success, result
            except sqlite3.OperationalError as e:
                es = 'no such table: '
                if e.args[0].startswith(es):
                    table_name = e.args[0][len(es):]
                    print('Table "{}" not currently present in the database'.format(table_name))
                    return Database.Result.TableMissing, table_name
                raise e
        return wrap_function

    @connection_decorator
    @missing_table_decorator
    def select_query(self, query, column_types, connection, cursor, do_print=False):
        it = cursor.execute(query)

        bp_table = boxes_pb2.Table(columns=[])
        is_digits = []
        for i, row in enumerate(it):
            for j,item in enumerate(row):
                if i == 0:
                    bp_table.columns.append(boxes_pb2.ColumnValues(str_values=[], num_values=[]))
                    is_digits.append(bool(j < len(column_types) and (column_types[j] == boxes_pb2.ColumnType.REAL or column_types[j] == boxes_pb2.ColumnType.INTEGER)))

                if is_digits[j]:
                    bp_table.columns[j].num_values.append(float(item) if item is not None else float('nan'))
                else:
                    bp_table.columns[j].str_values.append(str(item) if item is not None else '')
                if do_print:
                    print('{:>23}'.format('None' if item == None else str(item)), end='')
            if do_print:
                print('')
        return bp_table

    @connection_decorator
    @missing_table_decorator
    def print_table(self, table_name, connection, cursor, full_print=False):
        print('----------- ' + table_name + ' ----------')

        cursor.execute('PRAGMA table_info("{}")'.format(table_name))
        print_db_row([e[1] + ' ' + e[2] for e in cursor.fetchall()])

        cursor.execute('SELECT * FROM "{}"'.format(table_name))
        print_db_rows(cursor.fetchall() if full_print else cursor.fetchmany())

    @connection_decorator
    def create_table(self, name, dataframe, connection, cursor):
        dataframe.to_sql(name=name, con=connection, index = False)

        '''
        create_string = "CREATE TABLE '{tn}' ({cols});".format(
            tn=name,
            cols=', '.join([quoted(cs.name) + ' ' + ct_to_str(cs.type) for cs in proto_schema.column_schemas]))
        cursor.execute(create_string)

        def value_gen(pts, pt):
            nof_rows = max(len(pt.columns[0].str_values), len(pt.columns[0].num_values))
            for i in range(nof_rows):
                t = tuple([c_to_str(cs.type, cv, i) for (cs, cv) in zip(pts.column_schemas, pt.columns)])
                yield t

        insert_string = "INSERT INTO '{tn}' ({cols}) VALUES ({vals});".format(
            tn = name,
            cols = ', '.join([quoted(cs.name) for cs in proto_schema.column_schemas]),
            vals = ','.join('?' * len(proto_schema.column_schemas)))
        cursor.executemany(insert_string, value_gen(proto_schema, proto_table))

        connection.commit()
        '''

