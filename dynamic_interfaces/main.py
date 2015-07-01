"""
Use case: A client is instantiated using something resembling a factory
pattern. The class of the client isn't known until execution. While the
interfaces (method signatures) of the clients are *very* similar, they don't
line up 100%.

One Possible Approach

On the surface, this scenario appears to be a use case for *args and/or
**kwargs. The problem with that approach is how does the calling code know
what, if anything, it should include in each?
"""
import random


class BaseClient(object):
    """

    """
    pass


class FooClient(BaseClient):
    """
    Talk to the ``Foo`` service about some widgets.
    """
    def get_widgets(self, username):
        """
        Return widgets related to ``username``.

        NOTE: Only ``username`` is needed.
        """
        return {
            'widgets': [random.randint(1, 100) for x in range(0, random.randint(1,10))],
            'username': username
        }


class BarClient(BaseClient):
    """
    Talk to the ``Bar`` service about some widgets.
    """
    def get_widgets(self, username, email):
        """
        Return widgets related to ``username`` and ``email``.

        NOTE: Both ``username`` and ``email`` are needed.
        """
        return {
            'widgets': [random.randint(1, 100) for x in range(0, random.randint(1,10))],
            'username': username
        }


def client_factory():
    """
    Return class of the client to be used.
    """
    client_map = {
        1: FooClient,
        2: BarClient
    }
    return client_map.get(random.randint(1, 2), FooClient)


def main():
    client_kls = client_factory()
    client = client_kls()

    widgets = client.get_widgets()
    print widgets


if __name__ == '__main__':
    main()    
