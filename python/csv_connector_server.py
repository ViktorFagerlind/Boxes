import pandas as pd 


from concurrent import futures
import logging

import grpc

import table_pb2
import table_pb2_grpc

from pandas.api.types import is_numeric_dtype


class CsvConnector(table_pb2_grpc.TableQueryServicer):

  def GetTable(self, request, context):
    swim_data = pd.read_csv('../input/' + request.name)#, usecols=['Intervaller', 'Längder', 'Sträcka', 'Tid', 'Total tid', 'Medeltempo', 'Medel-Swolf', 'Totalt antal simtag'])

    csv_table = table_pb2.Table(header=[], row=[])

    for col in swim_data.columns:
        t = table_pb2.ColumnType.DECIMAL if(is_numeric_dtype(swim_data[col])) else table_pb2.ColumnType.STRING
        h = table_pb2.CsvHeader(name=col, type=t)

        csv_table.header.append(h)
        #logging.debug(t)
        #logging.debug(h)

    for i, row in swim_data[:2].iterrows():
        index=0
        csv_row = table_pb2.CsvRow(value=[])
        for j, item in row.items():
            #logging.debug('index ' + str(index))
            #logging.debug('item ' + str(item))
            #logging.debug('type ' + str(csv_table.header[index].type) + '\n')

            if csv_table.header[index].type == table_pb2.ColumnType.DECIMAL:
                v = table_pb2.CsvValue(decimal_value=item)
            else:
                v = table_pb2.CsvValue(string_value=str(item))
            csv_row.value.append(v)
            index = index + 1

        csv_table.row.append(csv_row)

    #logging.debug(csv_table)

    return csv_table


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    table_pb2_grpc.add_TableQueryServicer_to_server(CsvConnector(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    serve()
    #cc = CsvConnector()
    #cc.GetTable(table_pb2.Query(name='swim.csv'), None)