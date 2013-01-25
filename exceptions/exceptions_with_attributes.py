class CustomException(Exception):
    """
    A custom excpetion with an __init__ that takes an arg and stores it for
    use in an `except` clause.
    """

    def __init__(self, *args, **kwargs):
        self.foo = kwargs.pop('foo', None)
        super(CustomException, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    try:
        raise CustomException(foo='asdf')
    except CustomException, e:
        print e.foo
