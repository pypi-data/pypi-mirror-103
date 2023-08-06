try:
    import logging
    import sys
    import datetime
    import os
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))

def Setlog():
    fmt = logging.Formatter('%(asctime)s - %(message)s')
    logger = logging.getLogger("{}".format(sys.argv[0]))
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(fmt)

    try:
        filesuffex = '.'.join(os.path.basename(sys.argv[0]).split('.')[:-1]) + '-'
    except:
        filesuffex = ''
    file_handler = logging.FileHandler('/tmp/{0}{1}.log'.format(filesuffex,datetime.date.today().strftime('%Y%m%d')))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
