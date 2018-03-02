# coding: utf


def pattern(func):
    """

    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.is_pattern = True
    return wrapper
