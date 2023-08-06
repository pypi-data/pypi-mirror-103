import sys
import cartils.enums as enums
import os
import colorama

FAILURE_BASE = '[FAILURE]'
SUCCESS_BASE = '[SUCCESS]'
ERROR_BASE = '[ERROR]'
WARN_BASE = '[WARN]'
INFO_BASE = '[INFO]'
DEBUG_BASE = '[DEBUG]'
TRACE_BASE = '[TRACE]'

FAILURE_PREFIX = f'{enums.Colors.BOLD.value}{enums.Colors.RED.value}{FAILURE_BASE}{enums.Colors.RESET.value} '
SUCCESS_PREFIX = f'{enums.Colors.BOLD.value}{enums.Colors.GREEN.value}{SUCCESS_BASE}{enums.Colors.RESET.value} '
ERROR_PREFIX   = f'{enums.Colors.RED.value}{ERROR_BASE}{enums.Colors.RESET.value} '
WARN_PREFIX    = f'{enums.Colors.YELLOW.value}{WARN_BASE}{enums.Colors.RESET.value} '
INFO_PREFIX    = f'{enums.Colors.BLUE.value}{INFO_BASE}{enums.Colors.RESET.value} '
DEBUG_PREFIX   = f'{enums.Colors.CYAN.value}{DEBUG_BASE}{enums.Colors.RESET.value} '
TRACE_PREFIX   = f'{enums.Colors.MAGENTA.value}{TRACE_BASE}{enums.Colors.RESET.value} '

class Logger:
    def __init__(self, log_level):
        colorama.init()
        if log_level == 'NONE':
            self.LOG_LEVEL = enums.LogLevel.NONE.value
        elif log_level == 'FAILURE':
            self.LOG_LEVEL = enums.LogLevel.SUCCESS.value
        elif log_level == 'SUCCESS':
            self.LOG_LEVEL = enums.LogLevel.SUCCESS.value
        elif log_level == 'ERROR':
            self.LOG_LEVEL = enums.LogLevel.ERROR.value
        elif log_level == 'INFO':
            self.LOG_LEVEL = enums.LogLevel.INFO.value
        elif log_level == 'WARN':
            self.LOG_LEVEL = enums.LogLevel.WARN.value
        elif log_level == 'DEBUG':
            self.LOG_LEVEL = enums.LogLevel.DEBUG.value
        elif log_level == 'TRACE':
            self.LOG_LEVEL = enums.LogLevel.TRACE.value        

    def FAILURE(self, message):
        if self.LOG_LEVEL >= enums.LogLevel.FAILURE.value:
            print('{}{}'.format(FAILURE_PREFIX, message))

    def SUCCESS(self, message):
        if self.LOG_LEVEL >= enums.LogLevel.SUCCESS.value:
            print('{}{}'.format(SUCCESS_PREFIX, message))

    def ERROR(self, message):
        if self.LOG_LEVEL >= enums.LogLevel.ERROR.value:
            print('{}{}'.format(ERROR_PREFIX, message))

    def WARN(self, message):
        if self.LOG_LEVEL >= enums.LogLevel.WARN.value:
            print('{}{}'.format(WARN_PREFIX, message))

    def INFO(self, message):
        if self.LOG_LEVEL >= enums.LogLevel.INFO.value:
            print('{}{}'.format(INFO_PREFIX, message))

    def DEBUG(self, message):
        if self.LOG_LEVEL >= enums.LogLevel.DEBUG.value:
            print('{}{}'.format(DEBUG_PREFIX, message))
    
    def TRACE(self, message):
        if self.LOG_LEVEL >= enums.LogLevel.TRACE.value:
            print('{}{}'.format(TRACE_PREFIX, message))

if __name__ == '__main__':
    logger = Logger('TRACE')
    logger.FAILURE("failure test")
    logger.SUCCESS("success test")
    logger.ERROR("error test")
    logger.WARN("warn test")
    logger.INFO("info test")
    logger.DEBUG("debug test")
    logger.TRACE("trace test")