import random
import pandas as pd
import logging
import grpc
import zipfile

from os import path
from fitparse import FitFile
from concurrent import futures
from df_prototables import df_to_prototable, df_to_protoschema
from consul_services import consul_register, consul_unregister
from garminconnect import Garmin

import boxes_pb2_grpc, boxes_pb2

class GarminConnector(boxes_pb2_grpc.ConnectorServicer):
    def __init__(self):
        self.table_to_df = {}

        self.activity_to_table_types = {'lap_swimming':['swim_lengths', 'swim_laps']}
        self.activities_table_name = 'activities'

        self.client = Garmin('viktor_fagerlind@hotmail.com', '6iZoXg4EooP3dpUg')
        self.client.login()

        self.activity_df = self.__activities_to_df(self.client.get_activities(start=0, limit=3))
        print(self.activity_df)

    def __activities_to_df(self, activities):
        cols = ['activityId', 'activityName', 'startTimeLocal', 'activityType']
        dict = {}
        for c in cols:
            dict[c] = []
        for a in activities:
            for c in cols[:-1]:
                dict[c].append(a[c])
            dict[cols[-1]].append(a[cols[-1]]['typeKey']) # Special handling of activity type since it is not a straight name:val pair

        return pd.DataFrame(data=dict, columns=cols)

    def __get_table_df(self, activity_id_and_type):
        if not activity_id_and_type in self.table_to_df:
            self.table_to_df[activity_id_and_type] = self.__get_table_df_no_cache(activity_id_and_type)
        return self.table_to_df[activity_id_and_type]


    def __get_table_df(self, activity_id_and_type):
        activity_id   = activity_id_and_type.split(':')[0]
        activity_type = activity_id_and_type.split(':')[1]

        zip_filename = f'./tmp/{str(activity_id)}.zip'
        if not path.exists(zip_filename):
            zip_data = self.client.download_activity(activity_id, dl_fmt=self.client.ActivityDownloadFormat.ORIGINAL)
            with open(zip_filename, "wb") as fb:
                print('------ ' + zip_filename + ' ------')
                fb.write(zip_data)

        fit_filename = f'./tmp/{str(activity_id)}.fit'
        if not path.exists(fit_filename):
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall('./tmp')

        fitfile = FitFile(fit_filename)
        fitfile.parse()


        table_type_info = {'swim_lengths':('lap',    ['avg_cadence', 'total_distance', 'total_elapsed_time', 'timestamp']),
                           'swim_laps':   ('length', ['avg_swimming_cadence', 'total_strokes', 'total_elapsed_time', 'timestamp'])}
        (info_type,fields) = table_type_info[activity_type]

        dict = {}
        for f in fields:
            dict[f] = []
        for msg in fitfile.get_messages(info_type, as_dict=False):
            # Go through all the data entries in this record
            for field in msg:
                if field.name in fields:
                    dict[field.name].append(field.value)

        return pd.DataFrame(data=dict, columns=fields)

    def GetTableNames(self, request, context):
        table_names = [self.activities_table_name]

        for i,row in self.activity_df.iterrows():
            activity_type = row['activityType']
            if activity_type in self.activity_to_table_types:
                for table_type in self.activity_to_table_types[activity_type]:
                    table_names.append(str(row['activityId']) + ':' + table_type)
            else:
                print('Activity type \'' + activity_type + '\' not supported (yet?).')

        return boxes_pb2.TableNames(table_names=table_names)


    def GetTableSchemas(self, request, context):
        ts = boxes_pb2.TableSchemas(table_schemas=[])

        for name in request.table_names:
            if name == self.activities_table_name:
                ts.table_schemas.append(df_to_protoschema(self.activity_df))
            else:
                ts.table_schemas.append(df_to_protoschema(self.__get_table_df(name)))

        return ts


    def GetTable(self, request, context):
        if request.name == self.activities_table_name:
            return df_to_prototable(self.activity_df)
        else:
            return df_to_prototable(self.__get_table_df(request.name))


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    boxes_pb2_grpc.add_ConnectorServicer_to_server(GarminConnector(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        server.wait_for_termination()
    except:
        print('User aborted')


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    port = random.randint(50000, 59000)

    name = 'Connector'
    consul_register(name, port)
    serve(port)
    consul_unregister(name, port)
