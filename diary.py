# ------------------------------------------------------------
#               Diary Function
# ------------------------------------------------------------

import logging


def diary(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Reset logger handlers, otherwise it will be written
    # several times into file/console
    if logger.handlers:
        logger.handlers = []

    fileHandler = logging.FileHandler(filename)
    consoleHandler = logging.StreamHandler()
    logger.addHandler(consoleHandler)
    formatter = logging.Formatter("%(message)s")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger, fileHandler, consoleHandler


def closeHandlersDiary(fileHandler, consoleHandler):
    fileHandler.close()
    consoleHandler.close()
    return
