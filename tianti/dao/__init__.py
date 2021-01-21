#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from psycopg2 import extras
from psycopg2 import connect
from tianti.conf import cfg
from tianti.common.logger import logger


class PostgresBaseDao(object):
    def __init__(self, host, user, password, database, port=5432):
        info = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port,
        }
        self.conn = connect(**info)
        self.curs = self.conn.cursor(cursor_factory=extras.RealDictCursor)

    def __del__(self):
        self.conn.close()

    def _execute(self, sql, data_tuple):
        try:
            self.curs.execute(sql, data_tuple)
            if sql.lstrip().lower().startwith("select"):
                result = self.curs.fetchall()
            else:
                self.conn.commit()
                result = True
            return result
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            raise e

    def execute(self, sql, data_tuple=None):
        return self._execute(sql, data_tuple)

    def query_page(self, sql, parameters=None, limit=None, page=None):
        try:
            offset = int(limit) * (int(page) - 1) if limit and page else None
            if offset is not None:
                suffix = " limit %s offset %s" % (limit, offset)
                sql +=  suffix

            self.curs.execute(sql, parameters)
            rows = self.curs.fetchall()
            return {"count": len(rows), "rows": self.format_data(rows)}
        except Exception as e:
            logger.error("%s query db failed. [%s]" % (sql, e))
            raise e

    @staticmethod
    def format_data(data):
        if isinstance(data, list):
            for d in data:
                for k, v in d.items():
                    if isinstance(v, datetime):
                        d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, datetime):
                    data[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        return data


class PostgresDao(PostgresBaseDao):
    def __init__(self):
        config = cfg.get_config("postgres")
        host = config.get("host")
        port = config.get("port")
        user = config.get("user")
        password = config.get("password")
        database = config.get("database")
        super(PostgresDao, self).__init__(host, user, password, database, port)


if __name__ == '__main__':
    pg = PostgresDao()
    sql = "select * from test"
    pg.execute(sql)
