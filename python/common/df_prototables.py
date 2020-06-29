import pandas as pd
from pandas.api.types import is_numeric_dtype

from common import boxes_pb2


def df_to_prototable(df):
    prototable = boxes_pb2.Table(columns=[])

    for col in df.columns:
        if (is_numeric_dtype(df[col])):
            dv = df[col].to_list()
            sv =[]
        else:
            sv = map(str, df[col].to_list())
            dv =[]

        prototable.columns.append(boxes_pb2.ColumnValues(str_values=sv, num_values=dv))

    return prototable


def df_to_protoschema(df):
    protoschema = boxes_pb2.TableSchema(column_schemas=[])

    for column_name in df.columns:
        df_type = df[column_name].dtype
        if df_type == int:
            t = boxes_pb2.ColumnType.INTEGER
        elif df_type == float:
            t = boxes_pb2.ColumnType.REAL
        else:
            t = boxes_pb2.ColumnType.STRING

        protoschema.column_schemas.append(boxes_pb2.ColumnSchema(name=column_name, type=t))

    return protoschema


def prototable_to_df(schema, table):
    df = pd.DataFrame()

    for s, c in zip(schema.column_schemas,table.columns):
        if s.type == boxes_pb2.ColumnType.INTEGER or s.type == boxes_pb2.ColumnType.REAL:
            df[s.name] = c.num_values
        else:
            df[s.name] = c.str_values

        if s.type == boxes_pb2.ColumnType.INTEGER:
            df[s.name] = df[s.name].astype(int)
        elif s.type == boxes_pb2.ColumnType.REAL:
            df[s.name] = df[s.name].astype(float)
        else:
            df[s.name] = df[s.name].astype(str)

    return df
