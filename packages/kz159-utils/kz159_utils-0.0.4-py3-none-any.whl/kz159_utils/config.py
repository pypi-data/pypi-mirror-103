import contextlib
from copy import deepcopy
from os import getenv, chdir
from os.path import abspath, dirname


class Config:
    def __init__(self, abs_path, service_name: str = __name__, ):
        self.try_to_load_dot_env(abs_path)
        self.SERVICE_NAME = service_name
        self.POSTGRES_HOST = getenv('POSTGRES_HOST', 'localhost')
        self.POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'postgres')
        self.POSTGRES_PORT = getenv('POSTGRES_PORT', '5432')
        self.POSTGRES_USER = getenv('POSTGRES_USER', 'postgres')
        self.POSTGRES_DB_NAME = getenv('POSTGRES_DB_NAME', 'postgres')
        self.LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')

    @staticmethod
    def try_to_load_dot_env(abs_path):
        try:
            # noinspection PyUnresolvedReferences
            from dotenv import load_dotenv

            abs_path = abspath(abs_path)
            dname = dirname(dirname(abs_path))
            chdir(dname)
            return load_dotenv('.env')
        except ImportError:
            pass
        # add here rmq/etc

    @property
    def postgres_dsn(self):
        return (f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}')

    @property  # do we need this?
    def test_postgres_db(self):
        return f'{self.POSTGRES_DB_NAME}_test'

    @contextlib.contextmanager
    def change_varible(self, key, value):
        _class = deepcopy(self)
        setattr(_class, key, value)
