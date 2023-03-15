from utils.logger import Logg
from utils.timer import Timer


class DoLog:
    @classmethod
    def do_log(cls):
        log = Logg.get_logger(f'log/{Timer.get_timestamp()}.log')
        return log
