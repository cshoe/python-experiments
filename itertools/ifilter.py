from itertools import ifilter


def filter_func(x):
    return x < 5


def main():
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print list(ifilter(filter_func, numbers))


if __name__ == '__main__':
    main()
