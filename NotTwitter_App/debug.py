from logging import Logger, FileHandler, DEBUG


# debug_mode == True일 때만 작동하는 로거 클래스
class MyLogger(Logger):
    def __init__(self, onoff, name=None, level=DEBUG, save_path='app_log.log'):
        super(MyLogger, self).__init__(name, level)
        self.__onoff = onoff
        if onoff == True:
            self.addHandler(FileHandler(save_path))
    def debug(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def info(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def warning(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def error(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def critical(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
logger = MyLogger(True)
