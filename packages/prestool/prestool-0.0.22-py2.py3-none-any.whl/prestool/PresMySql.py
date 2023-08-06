from .util import format_quot_str_util, make_sql_str_util
import pymysql


class SqlStr:
    @staticmethod
    def select_sql_str(table, target=None, where=None):
        return make_sql_str_util('select', table, select_target=target, where=where)

    @staticmethod
    def update_sql_str(table, target, where):
        return make_sql_str_util('update', table, update_target=target, where=where)

    @staticmethod
    def delete_sql_str(table, where):
        return make_sql_str_util('delete', table, where=where)

    @staticmethod
    def insert_sql_str(table, target):
        return make_sql_str_util('insert', table, target)


class PresMySql(SqlStr):
    def __init__(self):
        self.mysql_host = ''
        self.mysql_port = ''
        self.mysql_user = ''
        self.mysql_pwd = ''
        self.mysql_db_name = ''
        self.mysql_charset = ''

    def connect(self):
        return pymysql.connect(
            host=self.mysql_host, user=self.mysql_user, password=self.mysql_pwd,
            db=self.mysql_db_name, charset=self.mysql_charset, port=self.mysql_port,
            cursorclass=pymysql.cursors.DictCursor)

    def get_db_info(self, table, target=None, where=None):
        sql = self.select_sql_str(table, target, where)
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result, sql
