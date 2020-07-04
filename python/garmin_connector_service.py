import logging
import random
import zipfile
import grpc
import argparse
import numpy
import pandas as pd

from fitparse import FitFile
from garminconnect import Garmin
from concurrent import futures
from os import path

from common import boxes_pb2_grpc
from common import boxes_pb2
from common.consul_services import consul_register, consul_unregister
from common.df_prototables import df_to_prototable, df_to_protoschema
from datetime import date, timedelta

table_type_info = {'swim_lengths': ('lap', ['avg_cadence', 'total_distance', 'total_elapsed_time', 'timestamp'], [float, int, float, str]),
                   'swim_laps': ('length', ['avg_swimming_cadence', 'total_strokes', 'total_elapsed_time', 'timestamp'], [float, float, float, str])}

all_activities_name = 'all_activities'

separator = '#'

class GarminConnector(boxes_pb2_grpc.ConnectorServicer):
    def __init__(self, nof_activities):
        self.activity_to_table_types = {'lap_swimming':['swim_lengths', 'swim_laps']}

        self.client = Garmin('viktor_fagerlind@hotmail.com', '6iZoXg4EooP3dpUg')
        self.client.login()

        self.table_names = []
        self.table_to_df = {}

        self.__setup_heart_rates(date(2018,9,1))
        self.__setup_activities(nof_activities)
        self.__setup_activity_table_names()

    def __add_table(self, name, df):
        self.table_names.append(name)
        self.table_to_df[name] = df

    def __setup_activity_table_names(self):
        for table_types in self.activity_to_table_types.values():
            for table_type in table_types:
                self.table_names.append(table_type)

        for i,row in self.table_to_df[all_activities_name].iterrows():
            activity_type = row['activityType']
            if activity_type in self.activity_to_table_types:
                for table_type in self.activity_to_table_types[activity_type]:
                    self.table_names.append(str(row['activityId']) + separator + table_type)
            else:
                print('Activity type \'' + activity_type + '\' not supported (yet?).')

    def __setup_activities(self, nof_activities):
        activities = self.client.get_activities(start=0, limit=nof_activities)
        column_names = ['activityId', 'activityName', 'startTimeLocal', 'distance', 'elapsedDuration', 'movingDuration', 'poolLength', 'activityType']
        column_types = [int, str, numpy.datetime64, str]
        data_dict = {}
        for c in column_names:
            data_dict[c] = []
        for a in activities:
            for c in column_names[:-1]:
                data_dict[c].append(a[c])
            data_dict[column_names[-1]].append(a[column_names[-1]]['typeKey']) # Special handling of activity type since it is not a straight name:val pair

        dataframe =  pd.DataFrame(data=data_dict, columns=column_names)
        for (column, column_type) in zip(column_names, column_types):
            dataframe[column] = dataframe[column].astype(column_type)

        self.__add_table(all_activities_name, dataframe)
        print(dataframe)

    def __setup_heart_rates(self, start_date):
        column_names = ['calendarDate', 'maxHeartRate', 'minHeartRate', 'restingHeartRate', 'lastSevenDaysAvgRestingHeartRate']
        column_types = [numpy.datetime64, float, float, float, float]

        data_dict = {}
        for c in column_names:
            data_dict[c] = []

        end_date = date.today()
        delta = end_date - start_date
        i = 0
        while i < delta.days:
            day = end_date - timedelta(days=i)
            heart_day = self.client.get_heart_rates(day.isoformat())
            if not None in heart_day.values():
                for c in column_names:
                    data_dict[c].append(heart_day[c])
            i = i + 7
            print (' ' + str(i), end='')

        dataframe =  pd.DataFrame(data=data_dict, columns=column_names)
        for (column, column_type) in zip(column_names, column_types):
            dataframe[column] = dataframe[column].astype(column_type)

        self.__add_table('heart_rates', dataframe)
        print(dataframe)

    def __get_table_type_metatable(self, type_name):
        new_df = None

        for name in self.table_names:
            name_parts = name.split(separator)
            if len(name_parts) > 1 and name_parts[1] == type_name:
                try:
                    tdf = self.__get_table_df(name).copy()
                except Exception as e:
                    print('Exception when retreiving table {}:{}'.format(name, e))
                    continue
                tdf['activityId'] = name_parts[0]
                if new_df is None:
                    new_df = tdf
                else:
                    new_df = pd.concat([new_df, tdf])
        return new_df


    def __get_table_df(self, table_name):
        if not table_name in self.table_to_df:
            if table_name in table_type_info:
                self.table_to_df[table_name] = self.__get_table_type_metatable(table_name)
            else:
                self.table_to_df[table_name] = self.__get_table_df_no_cache(table_name)
        return self.table_to_df[table_name]


    def __get_table_df_no_cache(self, activity_id_and_type):
        activity_id   = activity_id_and_type.split(separator)[0]
        activity_type = activity_id_and_type.split(separator)[1]

        zip_filename = f'./tmp/{str(activity_id)}.zip'
        if not path.exists(zip_filename):
            zip_data = self.client.download_activity(activity_id, dl_fmt=self.client.ActivityDownloadFormat.ORIGINAL)
            print('Downloding {}...'.format(zip_filename))
            with open(zip_filename, "wb") as fb:
                fb.write(zip_data)

        fit_filename = f'./tmp/{str(activity_id)}.fit'
        if not path.exists(fit_filename):
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                print('Extracting {}...'.format(zip_filename))
                zip_ref.extractall('./tmp')

        fitfile = FitFile(fit_filename)
        print('Parsing    {}...'.format(fit_filename))
        fitfile.parse()

        (info_type,column_names, column_types) = table_type_info[activity_type]

        data_dict = {}
        for f in column_names:
            data_dict[f] = []
        for msg in fitfile.get_messages(info_type, as_dict=False):
            # Go through all the data entries in this record
            for field in msg:
                if field.name in column_names:
                    data_dict[field.name].append(field.value)

        dataframe = pd.DataFrame(data=data_dict, columns=column_names)
        for (column, column_type) in zip(column_names, column_types):
            dataframe[column] = dataframe[column].astype(column_type)

        return dataframe

    def GetTableNames(self, request, context):
        return boxes_pb2.TableNames(table_names=self.table_names)

    def GetTableSchemas(self, request, context):
        ts = boxes_pb2.TableSchemas(table_schemas=[])

        for name in request.table_names:
            ts.table_schemas.append(df_to_protoschema(self.__get_table_df(name)))

        return ts


    def GetTable(self, request, context):
        return df_to_prototable(self.__get_table_df(request.name))


def serve(port, num_items):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    boxes_pb2_grpc.add_ConnectorServicer_to_server(GarminConnector(num_items), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        server.wait_for_termination()
    except:
        print('User aborted')


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--numitems', default=1000, help="Total number of items to retreive from garmin")
    args = parser.parse_args()

    port = random.randint(50000, 59000)

    name = 'Connector'
    consul_register(name, port)
    serve(port, args.numitems)
    consul_unregister(name, port)
