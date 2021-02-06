# -*- coding: utf-8 -*-
import os
import sqlite3
from typing import (
    Tuple, List, TypeVar
)

Self = TypeVar('Self', bound='Database')


class Database:
    def __enter__(self) -> Self:
        self.database = os.path.join(os.getcwd(), 'info.db')
        if os.path.isfile(self.database):
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
        else:
            self.conn, self.cursor = self.__create_db()
        return self

    def __create_db(self) -> Tuple:
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''create table sender_info(username vchar not null, 
                                                   passwd vchar not null, 
                                                   email_host vchar not null);''')
        cursor.execute('''insert into sender_info values('E-mail', 'password', 'E-mail host');''')

        cursor.execute('''create table proxy_server(proxy vchar not null, 
                                                    port int not null);''')
        cursor.execute('''insert into proxy_server values('127.0.0.1', 8080);''')

        cursor.execute('''create table recv_info(mail_addr vchar not null);''')

        return conn, cursor

    def sender_info_save(self, username: str, passwd: str, email_host: str) -> None:
        self.cursor.execute(f'''update sender_info set 
                                username="{username}",
                                passwd="{passwd}",
                                email_host="{email_host}";''')

    def sender_info_read(self) -> List[Tuple]:
        self.cursor.execute('''select * from sender_info;''')
        result = self.cursor.fetchall()
        return result

    def recv_info_append(self, receiver: str) -> None:
        self.cursor.execute(f'''insert into recv_info values("{receiver}");''')

    def recv_info_delete(self, receiver: str):
        self.cursor.execute(f'''delete from recv_info where mail_addr="{receiver}";''')

    def recv_info_read(self) -> List[Tuple]:
        self.cursor.execute('''select * from recv_info;''')
        result = self.cursor.fetchall()
        return result

    def proxy_save(self, proxy: str, port: int) -> None:
        self.cursor.execute(f'''update proxy_server set
                                proxy="{proxy}",
                                port={port};''')

    def proxy_read(self) -> List[Tuple]:
        self.cursor.execute('''select * from proxy_server;''')
        result = self.cursor.fetchall()
        return result

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # exc_type: 異常類型, exc_val: 異常值, exc_tb: 異常錯誤棧
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
        if exc_val is not None:
            print(exc_type, exc_val, exc_tb)
