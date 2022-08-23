import logging

# create formatter
formatter = logging.Formatter('%(asctime)s %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# ch.setLevel(logging.DEBUG)

# create logger
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)

# add formatter to ch and add ch to logger
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.debug("Logger created")


def getLogger():
    return logger
