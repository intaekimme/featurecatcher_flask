from config.default import *

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{pw}@{url}/{db}'.format(
    user='root',
    pw='',
    url='127.0.0.1',
    db='video_detector')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "dev"