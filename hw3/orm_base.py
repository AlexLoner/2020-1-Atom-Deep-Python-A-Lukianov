import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MyBase:
    '''Creata database and establish connection with it'''


    def __init__(self, db):
        self.db = db
        self.user = 'loner'
        self.password = 'password'
        self.connection = self.set_connection()
        self.session = sessionmaker(bind=self.connection.engine)()

    def set_connection(self):
        '''Create connection between db and python'''
        try:
            connection = sqlalchemy.create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@localhost:3306/{self.db}', encoding='utf8').connect()
        except sqlalchemy.exc.InternalError:
            connection = sqlalchemy.create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@localhost:3306/', encoding='utf8').connect()
            connection.execute(f'CREATE DATABASE {self.db}')
            connection.close()
            connection = sqlalchemy.create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@localhost:3306/{self.db}', encoding='utf8').connect()
        return connection
