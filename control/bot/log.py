import logging
from django.conf import settings


log_object = None

def logger():
    global log_object
    if log_object:
        return log_object

    level = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }.get(settings.LOG_VERBOSITY, logging.DEBUG)

    log = logging.getLogger(name=settings.LOG_PREFIX)
    log.setLevel(level)
    formatter = logging.Formatter(settings.LOG_FORMAT)

    fh = logging.FileHandler(settings.LOG_FILE)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)

    log_object = log
    return log


