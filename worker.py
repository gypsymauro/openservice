from openservice import openService
from datetime import datetime
import psycopg2
from psycopg2.extras import DictCursor
import logging
import configparser

#singleton db connection class
class DatabaseConnection:
    _instance = None

    def __init__(self):
        self.log = logging.getLogger(__name__)
        logging.basicConfig()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._connection = None
        return cls._instance    

#    def __del__(self):
#        if cls._instance is not None:
#            cls._instance._connection.close()
#            log.info('Database connection closed.')

    
    def connect(self, host, dbname, user, password):
        """
        Connect to the database using the provided credentials.
        """
        try:
            self._connection = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=user,
                password=password
            )
        except Exception as e:
            self.log.info(f"Failed to connect to database: {e}")

    def execute(self, query, params=None):
        """
        Execute a SQL query on the database.
        """
        if self._connection is None:
            self.log.error("Error: database connection not established")
            return None

        cursor = self._connection.cursor(cursor_factory=DictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()

        return result

    def disconnect(self):
        """
        Close the connection to the database.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            

class Worker(openService):
    
    def __init__(self):
        super().__init__()

        config = configparser.ConfigParser()
        config.read('worker.ini')
        hostname = config.get('default','hostname',fallback='localhost')
        dbname = config.get('default','dbname',fallback='postgres')
        username = config.get('default','username',fallback='postgres')
        password = config.get('default','password',fallback='password')        
        
        self.dc = DatabaseConnection()
        self.dc.connect(hostname,dbname,username,password)
        

    def createOrUpdateItem(self,data,modified_date):
        response=self.read(data['metadata']['remoteId'])
        if response.status_code == 200:
            remote_modified_date=datetime.strptime(response.json()['metadata']['modified'][0:10],'%Y-%m-%d')
            if modified_date.strftime("%Y%m%d")>remote_modified_date.strftime("%Y%m%d"):
                self.update(data)

            else:
                self.log.debug('already updated')
        else:
            self.create(data)

    def getDataset(self,query):
        ds = self.dc.execute(query)
        return ds

    def do(self):
        print('TODO')
        
      

if __name__ == "__main__":        
    worker = Worker()
    ds = worker.getDataset("select * from portale.www_consiglio_comunale")
    for record in ds:
        print(record)
    
#    print(worker.createOrUpdate())



