from itertools import chain


def main():
    letters = ['a', 'b', 'c', 'd']
    more_letters = ['z', 'y', 'x', 'w']

    print 'letters is: {}'.format(letters)
    print 'more_letters is: {}'.format(more_letters)

    chained = chain(letters, more_letters)

    print 'letters and more_letters chained is: {}'.format(list(chained))

if __name__ == '__main__':
    main()
