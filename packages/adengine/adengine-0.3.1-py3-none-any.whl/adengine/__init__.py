import logging
import sys
import os

log_level = os.environ.get('ADENGINE_LOG_LEVEL', 'INFO')
if log_level.upper() == 'DEBUG':
    LOG_LEVEL = logging.DEBUG
elif log_level.upper() == 'INFO':
    LOG_LEVEL = logging.INFO
elif log_level.upper() == 'WARNING':
    LOG_LEVEL = logging.WARNING
elif log_level.upper() == 'ERROR':
    LOG_LEVEL = logging.ERROR
else:
    raise Exception(f'Unknown log level: {log_level}')

logger = logging.getLogger('adengine')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(LOG_LEVEL)

logger.addHandler(handler)


__all__ = [
    'pt',
    'engine',
    'server',
    'client',
    'messages',
]
