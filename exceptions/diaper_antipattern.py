def main():
    key = None
    secret = None
    token = None
    
    try:
        key = '123'
        raise Exception('LOLIDK')
    except:
        pass

    print('key: {}'.format(key))
    print('secret: {}'.format(secret))
    print('token: {}'.format(token))

if __name__ == '__main__':
    main()
