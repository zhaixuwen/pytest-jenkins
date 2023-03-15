# -*- coding: utf-8 -*-
import logging


class Logg:

    @classmethod
    def get_logger(cls, file):
        logger = logging.getLogger("api")
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s', datefmt="%Y-%m-%d %X")
        fl = logging.FileHandler(filename=file, encoding='utf-8')
        fl.setFormatter(formatter)
        sl = logging.StreamHandler()
        sl.setFormatter(formatter)

        logger.addHandler(fl)
        logger.addHandler(sl)

        return logger
