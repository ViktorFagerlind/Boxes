import logging
import pandas as pd



import boxes_pb2

from pandas.api.types import is_numeric_dtype

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

    for col in df.columns:
        t = boxes_pb2.ColumnType.NUMBER if is_numeric_dtype(df[col]) else boxes_pb2.ColumnType.STRING
        protoschema.column_schemas.append(boxes_pb2.ColumnSchema(name=col, type=t))

    return protoschema


def prototable_to_df(schema, table):
    df = pd.DataFrame()

    for s, c in zip(schema.column_schemas,table.columns):
        if (s.type == boxes_pb2.ColumnType.NUMBER):
            df[s.name] = c.num_values
        else:
            df[s.name] = c.str_values
    return df
