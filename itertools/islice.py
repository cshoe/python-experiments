"""
Trying to figure out how islice works.
"""

from itertools import islice


def dumb_gen(start, end):
    """
    Generate some numbers.
    """
    for x in xrange(start, end):
        print 'SOME SLOW DB QUERY'
        yield x


def main():
    for x in list(islice(dumb_gen(1, 5000), 50, 100)):
        print x


if __name__ == '__main__':
    main()
