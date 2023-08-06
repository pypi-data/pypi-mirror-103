import logging
from logging.config import dictConfig


logging_config = dict(
    version=1,
    formatters={
        'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'},
        'n': {'format': '[%(asctime)s] {%(pathname)s: %(name)-12s %(lineno)d}'
                        '%(levelname)s - %(message)s'}
    },
    handlers={
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'n',
            'level': logging.DEBUG
        },
        'r': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'n',
            'level': logging.DEBUG,
            'filename': 'ocr.log',
            'maxBytes': 10000,
            'backupCount': 1
        }
    },
    root={
        'handlers': ['h', 'r'],
        'level': logging.DEBUG
    }
)

dictConfig(logging_config)


def logger(name):
    return logging.getLogger(name)
