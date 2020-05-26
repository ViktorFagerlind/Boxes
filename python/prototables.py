import logging
import pandas as pd



import table_pb2
import table_pb2_grpc

from pandas.api.types import is_numeric_dtype

def df_to_prototable(df):
    proto_table = table_pb2.Table(columns=[])

    for col in df.columns:
        if (is_numeric_dtype(df[col])):
            t = table_pb2.ColumnType.DECIMAL
            dv = df[col].to_list()
            sv =[]
        else:
            t = table_pb2.ColumnType.STRING
            sv = map(str, df[col].to_list())
            dv =[]

        proto_table.columns.append(table_pb2.Column(name=col, type=t, str_values=sv, dec_values=dv))

    return proto_table

def prototable_to_df(pt):
    df = pd.DataFrame()

    for c in pt.columns:
        if (c.type == table_pb2.ColumnType.DECIMAL):
            df[c.name] = c.dec_values
        else:
            df[c.name] = c.str_values
    return df
