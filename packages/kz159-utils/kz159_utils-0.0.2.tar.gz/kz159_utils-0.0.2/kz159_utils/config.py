from os import getenv, chdir
from os.path import abspath, dirname

try:
    from dotenv import load_dotenv

    abspath = abspath(__file__)
    dname = dirname(dirname(abspath))
    chdir(dname)

    load_dotenv('.env')
except ImportError:
    pass


class Config:
    def __init__(self, service_name: str = __name__):
        self.SERVICE_NAME = service_name
        self.POSTGRES_HOST = getenv('POSTGRES_HOST', 'localhost')
        self.POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'postgres')
        self.POSTGRES_PORT = getenv('POSTGRES_PORT', '5432')
        self.POSTGRES_USER = getenv('POSTGRES_USER', 'postgres')
        self.POSTGRES_DB_NAME = getenv('POSTGRES_DB_NAME', 'postgres')
        self.LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
        # add here rmq/etc

    @property
    def postgres_dsn(self):
        return (f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}')


class CustomLogger:
    # try to init logger from here
    pass

