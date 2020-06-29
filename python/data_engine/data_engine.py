import pandas as pd
from common.df_prototables import df_to_protoschema, df_to_prototable, prototable_to_df
from data_engine.connector_manager import ConnectorManager
from data_engine.algorithms import Algorithms
from data_engine.database import Database


class DataEngine:
    def missing_table_decorator(func):
        def wrap_function(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if result[0] == Database.Result.TableMissing:
                name = result[1]
                if not self.connector_manager.is_table_present(name):
                    raise Exception('Table "{}" is not available in any connector!'.format(name))
                self.__create_table(name)
                return wrap_function(self, *args, **kwargs)
            return result[1]
        return wrap_function

    def __init__(self):
        self.connector_manager = ConnectorManager()
        self.algorithms = Algorithms()
        self.database = Database()

        self.__setup_tablestable()

    def __setup_tablestable(self):
        name = 'all_tables'
        table_names = [name] + self.connector_manager.get_table_names()
        df = pd.DataFrame({'Table names':table_names, 'Cached':[False]*len(table_names)})

        self.database.create_table(name=name, dataframe=df)
        self.database.print_table(name, full_print=True)
        #print(df)


    def __create_table(self, name):
        ps = self.connector_manager.get_table_schema(name)
        pt = self.connector_manager.get_table(name)

        self.database.create_table(name=name, dataframe=prototable_to_df(ps, pt))
        print('Created table "{}"'.format(name))
        self.database.print_table(name)

    def __create_all_tables(self):
        for n in self.connector_manager.get_table_names():
            self.create_table(n)

    def print_algorithm_apply(self, query):
        # for key in ['Totalt antal simtag', 'Längder', 'avg_cadence']:
        # if key in df.columns:
        #    print('Average of %s: %f' % (key, self.algorithms.average(df[key])))
        pass    # TODO

    @missing_table_decorator
    def select_query(self, query, column_types):
        return self.database.select_query(query, column_types)







