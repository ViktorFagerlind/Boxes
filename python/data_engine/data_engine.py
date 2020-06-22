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

    def test(self):
        names = self.connector_manager.get_table_names()
        print(names)

        pts = self.connector_manager.get_table_schemas(names)

        for n, ps in zip(names, pts.table_schemas):
            pt = self.connector_manager.get_table(n)
            df = prototable_to_df(ps, pt)
            print(df)
            for key in ['Totalt antal simtag', 'Längder', 'avg_cadence']:
                if key in df.columns:
                    print('Average of %s: %f' % (key, self.algorithms.average(df[key])))
            print('\n')
