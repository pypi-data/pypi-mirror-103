import datetime
import logging

from functools import wraps
from secrets import token_hex


def log_this(level=None, filename=None, log_format=None, result_attrs=None):
    logger_name = token_hex(16)
    logger = logging.getLogger(logger_name)
    if level:
        logger.setLevel(level)
    else:
        level = logger.getEffectiveLevel()
    if filename:
        fhandler = logging.FileHandler(filename=filename)
        logger.addHandler(fhandler)
    else:
        shandler = logging.StreamHandler()
        logger.addHandler(shandler)
    if log_format:
        formatter = logging.Formatter(log_format, style='{')
        fhandler.setFormatter(formatter)
    
    def decorator(func):
        nonlocal result_attrs
        @wraps(func)
        def wrapper(*args, **kwargs):
            t0 = datetime.datetime.utcnow()
            result =  func(*args, **kwargs)
            t1 = datetime.datetime.utcnow()
            if result_attrs is not None:
                d = {func.__name__: func(result) for func in result_attrs}
                result_str = f' Result {d}'
            else:
                result_str = ''
            logger.log(level=level, msg=f'Calling: {func.__name__} [{t0}  {t1}] Args: {args} Kwargs: {kwargs}{result_str}')
            return result
        return wrapper
    return decorator
