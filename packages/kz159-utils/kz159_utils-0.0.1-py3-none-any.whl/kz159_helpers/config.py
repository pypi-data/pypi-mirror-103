from os import getenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    def __init__(self):
        self.POSTGRES_HOST = getenv('POSTGRES_HOST', 'localhost')
        self.POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'postgres')
        self.POSTGRES_PORT = getenv('POSTGRES_PORT', '5432')
        self.POSTGRES_USER = getenv('POSTGRES_USER', 'postgres')
        self.POSTGRES_DB_NAME = getenv('POSTGRES_DB_NAME', 'postgres')
        # add here rmq/etc

    @property
    def postgres_dsn(self):
        return (f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}')
