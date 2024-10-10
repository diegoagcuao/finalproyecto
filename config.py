import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = 'postgresql://flaskuser:password@localhost/linkscribe'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Pd13g0%402024@psclasificadoria.postgres.database.azure.com:5432/linkscribe'

