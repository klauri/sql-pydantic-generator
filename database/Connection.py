import sqlite3

class Connection:
    def __init__(self, connect) -> None:
        self.connect = connect('test.db')

    def execute(self, sql_stmt, values = None):
        cursor = self.connect.cursor()
        if not values:
            cursor.execute(sql_stmt)
        else:
            cursor.execute(sql_stmt, values)
        self.connect.commit()
        self.connect.close()
        return f'Executed SQL: {sql_stmt}'

    def select(self):
        cursor = self.connect.cursor()
        res = cursor.execute('pragma table_info("example")')
        return res.fetchone()


if __name__=='__main__':
    connection = Connection(sqlite3.connect)
    res = connection.select()
    print(res)