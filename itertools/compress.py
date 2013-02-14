from itertools import compress


def main():
    letters = ['a', 'b', 'c', 'd']
    booleans = [True, False, True, True]

    print 'letters is: {}'.format(letters)
    print 'booleans is: {}'.format(booleans)

    compressed = compress(letters, booleans)

    print 'letters and booleans compressed is: {}'.format(list(compressed))

    # what happens if the lists aren't the same length?
    # Answer: dictated by the boolean list.
    letters = ['a', 'b', 'c', 'd', 'e', 'f']
    booleans = [True, False, True, True]
    print 'letters is: {}'.format(letters)
    print 'booleans is: {}'.format(booleans)

    compressed = compress(letters, booleans)

    print 'letters and booleans compressed is: {}'.format(list(compressed))

    letters = ['a', 'b', 'c', 'd']
    booleans = [True, False, True, True, True, True]

    print 'letters is: {}'.format(letters)
    print 'booleans is: {}'.format(booleans)

    compressed = compress(letters, booleans)


if __name__ == '__main__':
    main()
