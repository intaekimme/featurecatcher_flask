from logging.config import dictConfig

from config.default import *


SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{pw}@{url}/{db}'.format(
    user='root',
    pw='',
    url='127.0.0.1',
    db='video_detector')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = b'Zb3\x81\xdb\xf1\xd9\xd7-Knb\x8eB\xa5\x18'

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/myproject.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
