import queue
import mysql.connector


class DbPool(object):
    def __init__(self, **kw):
        self.size = kw.get('size', 10)
        self.kw = kw
        self.conn_queue = queue.Queue(maxsize=self.size)
        for i in range(self.size):
            self.conn_queue.put(self._create_new_conn())

    def _create_new_conn(self):
        return mysql.connector.connect(
            host=self.kw.get('host'),
            port=self.kw.get('port'),
            user=self.kw.get('username'),
            password=self.kw.get('password'),
            database=self.kw.get('database')
        )

    def put_conn(self, conn):
        self.conn_queue.put(conn)

    def get_conn(self):
        conn = self.conn_queue.get()
        if conn is None:
            conn = self._create_new_conn()
        return conn
