def with_finally():
    print 'with_finally'
    try:
        raise KeyError()
    except KeyError:
        print 'KeyError raised'
    else:
        print 'Hit else'
    finally:
        print 'hit finally'


def return_in_else():
    print 'return_in_else'
    try:
        x = 1
    except KeyError:
        print 'KeyError raised'
    else:
        print 'Hit else and returning'
        return None
    finally:
        print 'hit finally'


if __name__ == '__main__':
    #with_finally()
    return_in_else()
