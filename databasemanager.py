import psycopg2
import logging
import hashlib
from psycopg2 import OperationalError

class DatabaseManager:
    def __init__(self, host:str, port:str, db:str, user:str, password:str) -> None:
        self._init_log()
        self._host = host
        self._db = db
        self._user = user
        self._password = password
        self._port = port
        self._connection = None
        
    def _init_log(self):
        self.__log = logging.getLogger(__name__)
        return
    
    def _create_connection(self)->bool:
        connection = None
        try:
            connection = psycopg2.connect(
                database=self._db,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
            )
            self.__log.info('[INFO]: Connection to PostgreSQL DB successful')
        
        except OperationalError as e:
            self.__log.error(f"The error '{e}' occurred")
            return False
        self._connection = connection
        return True
    
    def _is_connected(self):
        if self._connection is not True:
            return False
        return True
        
    def update_status(self, data:dict, status:bool=True):
        self.__log.info('[INFO]: update status appointment')
        ret = False
        if self._is_connected() is not True:
            self._create_connection()
        cursor = self._connection.cursor()
        query = """
            UPDATE {}
            SET status = %s
            WHERE  date = %s
            AND firstname = %s
            AND lastname = %s
            """.format('clientapp.appointments')
        try:
            cursor.execute(query, (status,
                                   data['date'],
                                   data['firstname'],
                                   data['lastname']) )
            self._connection.commit()
            ret = True
        finally:
            cursor.close()
        return ret
    
    def delete_row(self, data:dict, status:bool=True):
        self.__log.info('[INFO]: delete status appointment')
        ret = False
        if self._is_connected() is not True:
            self._create_connection()
        cursor = self._connection.cursor()
        query = """
            DELETE FROM {}
            WHERE  date = %s
            AND firstname = %s
            AND lastname = %s
            """.format('clientapp.appointments')
        try:
            cursor.execute(query, (data['date'],
                                   data['firstname'],
                                   data['lastname']) )
            self._connection.commit()
            ret = True
        finally:
            cursor.close()
        return ret

    
    def get_appointments(self, date:str):
        self.__log.info('[INFO]: Get available appointment')
        rows = None
        if self._is_connected() is not True:
            self._create_connection()
        cursor = self._connection.cursor()
        begin_date = date + ' 00:00:00'
        end_date = date + ' 23:59:59'
        query = """
            SELECT * FROM {}
            WHERE date >= '{}'
            AND date <= '{}'
            AND status = False
            ORDER BY date ASC
            """.format('clientapp.appointments', begin_date, end_date)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        finally:
            cursor.close()
        return rows
    
    def _insert_appointment(self, row:dict):
        self.__log.info(f"[INFO]: Insert appointment'{row}'")
        ret = False
        if self._is_connected() is not True:
            self._create_connection()
        cursor = self._connection.cursor()
        query = """
            INSERT INTO {}
            (firstname, lastname, date) 
            VALUES 
            (%s, %s, %s)
            """.format('clientapp.appointments')
        try:
            cursor.execute(query, (row['firstname'],
                                   row['lastname'],
                                   row['date']))
            self._connection.commit()
            ret = True
        finally:
            cursor.close()
        return ret
    
    def login(self, username:str, password:str) -> bool:
        ret = False
        username = username.encode('utf-8')
        password = password.encode('utf-8')
        hash_username = hashlib.sha256()
        hash_password = hashlib.sha256()
        hash_username.update(username)
        hash_password.update(password)
        if self._is_connected() is not True:
            self._create_connection()
        cursor = self._connection.cursor()
        query = """
            SELECT * FROM {}
            WHERE username = '{}'
            AND password = '{}'
            """.format('clientapp.users',
                        hash_username.hexdigest(),
                        hash_password.hexdigest())
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        finally:
            if len(rows) == 1:
                ret = True
            cursor.close()
        return ret
        

