from contextlib import contextmanager

class ClientContextManager(object):
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

    def __enter__(self):
        print("Entering client context manager {}".format(id(self)))

    def __exit__(self, type, value, traceback):
        print("Exiting client context manager")


class LocalContextManager(object):
    def __enter__(self):
        print("Entering local context manager {}".format(id(self)))

    def __exit__(self, type, value, traceback):
        print("Exiting local context manager")

    def make_child(self, local=True):
        if local is True:
            return LocalContextManager()
        return ClientContextManager()


class ServerContextManager(object):
    def __enter__(self):
        print("Entering server context manager")

    def __exit__(self, type, value, traceback):
        print("Exiting server context manager")

    def make_child(self, local=True):
        if local is True:
            return LocalContextManager()
        return ClientContextManager()


class ContextManagerUser(object):
    def __init__(self, server_mgr):
        self.server_mgr = server_mgr
        self._local_mgr = None

    def do_lots_of_things(self):
        with self._get_local_mgr() as local_mgr:
            for x in range(5):
                self.do_a_thing()

    def do_a_thing(self):
        with self.bottom_mgr().make_child(local=False) as mgr:
            print("doing stuff")

    @contextmanager
    def _get_local_mgr(self):
        self._local_mgr = self.server_mgr.make_child(local=True)
        yield self._local_mgr.__enter__()
        self._local_mgr.__exit__()
        self._local_mgr = None

    def bottom_mgr(self):
        if self._local_mgr is not None:
            return self._local_mgr
        return self.server_mgr


class OtherThing(object):
    def method_that_takes_a_ctx_mgr(self, foo, bar=False, ctx_mgr=None):
        if ctx_mgr is not None:
            with ctx_mgr as context:
                return self._actually_do_method(foo, bar=bar)

        return self._actually_do_method(foo, bar=bar)

    def _actually_do_method(foo, bar=False):
        return 'LOLOLOL'



def main():
    c = ClientContextManager('lol', True)
    thing = OtherThing()
    print(thing.method_that_takes_a_ctx_mgr('lol', bar=True, ctx_mgr=c))
    # server_mgr = ServerContextManager()
    # thing = ContextManagerUser(server_mgr)
    # thing.do_lots_of_things()

    # print("Done doing lots of stuff")

    # thing.do_a_thing()


if __name__ == '__main__':
    main()
