#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3 as lite

DATABASE_NAME = 'data_files/qtrainer.db'

def singleton(cls):
    def instance(data_base_name):
        if not '__instance' in cls.__dict__:
            cls.__dict__['instance'] = cls(data_base_name)
        return cls.__dict__['instance']
    return instance

@singleton
class DataBaseProcess:

    def __init__(self, data_base_name):
        self.conn = lite.connect(data_base_name)
        self.cur = self.conn.cursor()
            
        if not self.conn:
            raise Exception("Error: connection faild!")

    def getCurrentUserId(self, user_login, user_pass):
        self.cur.execute("select userid from user_login where user_login=? and user_pass=?", (user_login, user_pass))
        result = self.cur.fetchone()

        if result is not None:
            self.current_user_id = result[0]
            return self.current_user_id
        else:
            return None

    def getExerciseId(self):
        self.cur.execute("select exid from exercize")

        return self.cur.fetchall()

    def getCurrentExerciseId(self):
        self.cur.execute("select currexid from user_currex where userid=?", (self.current_user_id, ))

        return self.cur.fetchone()

    def getExerciseText(self, exid):
        self.cur.execute("select exercize from exercize where exid=?", (exid, ))

        return self.cur.fetchone()[0]

    def getStatData(self, current_userid, current_ex_id, statdata):
        self.cur.execute("select ? from statistic where userid=? and exid=?", (statdata, current_userid, current_ex_id))

        return self.cur.fetchone()

    def closeConnection(self):
        if self.conn:
            self.conn.close()


dbp = DataBaseProcess(DATABASE_NAME)







