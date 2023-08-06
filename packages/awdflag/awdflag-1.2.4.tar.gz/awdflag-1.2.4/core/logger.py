import logging
import sys
import datetime


def setLog():
    fmt = logging.Formatter('%(asctime)s - %(message)s')
    logger = logging.getLogger("{}".format(sys.argv[0]))
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(fmt)

    file_handler = logging.FileHandler('/tmp/{0}{1}.log'.format("AutoAwd", datetime.date.today().strftime('%Y%m%d')))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
