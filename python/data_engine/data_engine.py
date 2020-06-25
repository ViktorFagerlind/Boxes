from common.df_prototables import prototable_to_df
from data_engine.connector_manager import ConnectorManager
from data_engine.algorithms import Algorithms
from data_engine.database import Database


class DataEngine:
    def __init__(self):
        self.connector_manager = ConnectorManager()
        self.algorithms = Algorithms()
        self.database = Database()

    def __read_dbs(self):
        pass

    def __create_table(self, name):
        ps = self.connector_manager.get_table_schema(name)
        pt = self.connector_manager.get_table(name)
        self.database.create_table(name=name, proto_schema=ps, proto_table=pt)
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

    def select_query(self, query):
        result = self.database.select_query(query)
        if result[0] == Database.Result.TableMissing:
            name = result[1]
            if not self.connector_manager.is_table_present(name):
                raise Exception('Table "{}" is not available in any connector!'.format(nam))
            self.__create_table(name)
            self.select_query(query)


