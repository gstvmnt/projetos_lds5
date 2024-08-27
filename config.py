import os

SECRET_KEY = 'igni'

SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '',
        servidor = 'localhost',
        database = 'projeto_lds5'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'


