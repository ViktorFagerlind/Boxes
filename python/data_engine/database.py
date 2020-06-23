import sqlite3

from contextlib import closing
from common import boxes_pb2

def ct_to_str(ct):
    return "REAL" if ct == boxes_pb2.ColumnType.NUMBER else "TEXT"

def c_to_str(ct, cvs, i):
    return cvs.str_values[i] if ct == boxes_pb2.ColumnType.STRING else cvs.num_values[i]


class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(':memory:')
            print(sqlite3.version)
        except Exception as e:
            print(e)

    def __del__(self):
        self.conn.close()

    def print_select_query(self, query):
        with closing(self.conn.cursor()) as c:
            it = c.execute(query)
            print(query)
            for row in it:
                print(row)

    def create_table(self, name, proto_schema, proto_table):
        with closing(self.conn.cursor()) as c:
            create_string = "CREATE TABLE '{tn}' ({cols});".format(
                tn=name,
                cols=', '.join([cs.name + ' ' + ct_to_str(cs.type) for cs in proto_schema.column_schemas]))
            c.execute(create_string)

            def value_gen(pts, pt):
                nof_rows = max(len(pt.columns[0].str_values), len(pt.columns[0].num_values))
                for i in range(nof_rows):
                    t = tuple([c_to_str(cs.type, cv, i) for (cs, cv) in zip(pts.column_schemas, pt.columns)])
                    yield t

            insert_string = "INSERT INTO '{tn}' ({cols}) VALUES ({vals});".format(
                tn=name,
                cols=', '.join([cs.name for cs in proto_schema.column_schemas])
,
                vals=','.join('?' * len(proto_schema.column_schemas)))
            c.executemany(insert_string, value_gen(proto_schema, proto_table))

            self.conn.commit()

