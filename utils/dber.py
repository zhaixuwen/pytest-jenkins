# -*- coding: utf-8 -*-
import pymysql
import yaml
from sshtunnel import SSHTunnelForwarder


class DB:
    """
        env可输入的值有：
        1. qa -> qa的aws库
        2. prod -> prod的aws库
        3. prod_ali -> prod的阿里云库
        4. prod_hw -> prod的华为云库
    """
    with open('properties/db.yaml', 'r') as f:
        _db_prop = yaml.safe_load(f)

    def __init__(self, env, db):
        addr = None
        username = None
        password = None
        self.db = None
        self.server = None
        self.cursor = None

        if env.startswith('qa'):
            addr = self._db_prop['qa'][env]['addr']
            username = self._db_prop['qa'][env]['username']
            password = self._db_prop['qa'][env]['password']
            self.db = pymysql.connect(host=addr,
                                      user=username,
                                      password=password,
                                      database=db)
            self.cursor = self.db.cursor()

        elif env.startswith('prod'):
            addr = self._db_prop['prod'][env]['addr']
            username = self._db_prop['prod'][env]['username']
            password = self._db_prop['prod'][env]['password']

            if env.startswith('prod_ali'):
                # 阿里云振德连接
                jumpserver_ip = '1.1.1.1'
                pem_name = 'test.pem'
                print('走了prod_ali...')

            self.server = SSHTunnelForwarder(
                (jumpserver_ip, 22),  # B机器的配置
                ssh_username='ubuntu',
                ssh_pkey="/home/ubuntu/path/" + pem_name,
                remote_bind_address=(addr, 3306))
            self.server.start()
            print(self.server)
            try:
                self.db = pymysql.connect(host="127.0.0.1",
                                          port=self.server.local_bind_port,
                                          user=username,
                                          password=password,
                                          database=db)
                # print(self.db)
                self.cursor = self.db.cursor()
                # print(self.cursor)
            except:
                print("创建数据库连接失败,请检查!")

    def query_all(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def query_one(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        return results

    def exec_sql(self, sql):
        self.cursor.execute(sql)

    def commit_exec(self):
        self.db.commit()

    def close_conn(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()
        if self.server is not None:
            self.server.stop()
