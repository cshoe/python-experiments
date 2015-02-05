from functools import partial


def main():
    thing = partial(func_to_partial, foo='foo', baz='baz')
    import pdb; pdb.set_trace()
    thing('message thing')


def func_to_partial(message, foo='bar', baz='qwerty'):
    print foo
    print baz
    print message


if __name__ == '__main__':
    main()
