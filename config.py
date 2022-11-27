import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('smtp-relay.sendinblue.com')
    MAIL_PORT = int(os.environ.get('587') or 25)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME=os.environ.get('hpp.service@mail.com') 
    MAIL_PASSWORD = os.environ.get('JksnBh25w9QXpc3')
    ADMINS = ['hpp.service@mail.com']