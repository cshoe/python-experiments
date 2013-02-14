from itertools import imap


def mult(x, y):
    return x * y


def main():
    numbers = [1,2,3]
    other_numbers = [4,5,6]
    print list(imap(mult, numbers, other_numbers))

if __name__ == '__main__':
    main()

