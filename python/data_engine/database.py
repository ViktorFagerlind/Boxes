import sqlite3

from contextlib import closing

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(':memory:')
            print(sqlite3.version)
        except Exception as e:
            print(e)

    def __del__(self):
        self.conn.close()

    def execute_query(self):
        with closing(self.conn.cursor()) as c:
            it = c.execute("SELECT id, name, address, salary from COMPANY")
            for row in it:
                print("ID = ", row[0])
                print("NAME = ", row[1])
                print("ADDRESS = ", row[2])
                print("SALARY = ", row[3], "\n")

    def create_table(self, name, proto_schema, proto_table):
        with closing(self.conn.cursor()) as c:
            c.execute('''CREATE TABLE COMPANY
                         (ID INT PRIMARY KEY     NOT NULL,
                          NAME           TEXT    NOT NULL,
                          AGE            INT     NOT NULL,
                          ADDRESS        CHAR(50),
                          SALARY         REAL);''')

            c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
                VALUES (1, 'Paul', 32, 'California', 20000.00 )")

            c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
                VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

            c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
                VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

            c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
                VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")

            self.conn.commit()
