from functools import wraps

def dec(print_before='default before', print_after='default after'):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            print print_before
            result = func(*args, **kwargs)
            print print_after
            return result
        return wrapped
    return wrapper


def printer(print_before='asdf', print_after='qwer'):
    return dec(print_before, print_after)


@printer(print_after='printed after')
def thing():
    print 'printed in the middle'


if __name__ == '__main__':
    thing()
