"""
Messing around with the built in `type` function. Trying to internalize
how it is used to create classes.
"""


class EqualityTest(object):
    """
    Dumb object used to test equality.
    """
    def __init__(self, foo):
        self.foo = foo


def equality_test():
    """
    Use `type` to try construct an object that is equal to on constructed
    with a normal class.

    Doesn't appear that this can be done.

    TODO: Find out what is different about the objects.
    """
    print '**** Equality Test ****'

    TestClass = type('EqualityTest', (), {'foo': True})
    test_class_instance = TestClass()
    
    equality_test_instance = EqualityTest(True)

    foo_equal = equality_test_instance.foo == test_class_instance.foo
    print 'foo attrs are equal: {0}'.format(foo_equal)

    instances_equal = test_class_instance == equality_test_instance
    print 'instances are equal: {0}'.format(instances_equal)
    

if __name__ == '__main__':
    equality_test()
