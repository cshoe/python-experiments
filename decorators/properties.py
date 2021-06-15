class Thing(object):
    @property
    def size(self):
        return 5


def main():
    foo = Thing()
    print(foo.size)


if __name__ == '__main__':
    main()
