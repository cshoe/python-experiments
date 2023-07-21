class Foo:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(self.name)
        self.name = "qwer"

    def meet(self):
        b = Bar(self)
        b.hello()


class Bar:
    def __init__(self, foo: Foo) -> None:
        self.foo = foo

    def hello(self):
        self.foo.introduce()


def main():
    f = Foo("asdf")
    f.meet()
    f.meet()


if __name__ == "__main__":
    main()
