# Some nested dicts that represent our data store.
DATASTORE = {
    'thing1': {
        'size': 'big',
        'color': 'red',
        'shape': 'circle'
    },
    'thing2': {
        'size': 'small',
        'color': 'blue',
        'shape': 'circle'
    },
    'thing3': {
        'size': 'medium',
        'color': 'green',
        'shape': 'square'
    }
}
class DictSubclass(dict):
    """
    Is subclassing `dict` really all that bad? We shall find out.
    """

    def __init__(self, name):
        """
        Get data from DATASTORE that correspond to `name` and use the
        corresponding dict as initial data.
        """
        self.name = name
        thing_data = DATASTORE[name]
        return super(DictSubclass, self).__init__(thing_data)

    def __setitem__(self, key, val):
        """
        Set the value corresponding to `key` to `val`.
        """
        DATASTORE[self.name][key] = val
        return super(DictSubclass, self).__setitem__(key, val)


if __name__ == '__main__':
    d_sub = DictSubclass('thing1')
    d_sub['size'] = 'medium'

    print 'In datastore: {0}'.format(DATASTORE['thing1']['size'])
    print 'On object: {0}'.format(d_sub['size'])
