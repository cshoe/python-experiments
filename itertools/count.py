from itertools import count


def main():
    for x in count(10, 0.25):
        if x < 20:
            print x
        else:
            break

if __name__ == '__main__':
    main()
