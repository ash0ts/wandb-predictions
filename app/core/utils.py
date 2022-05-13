import functools

from loguru import logger


def logging_wrap(foo):
    @functools.wraps(foo)
    def _(*args, **kwargs):
        logger.opt(depth=1).debug(
            f"Calling {foo.__name__} with args {args} and kwargs {kwargs}")
        return foo(*args, **kwargs)

    return _
