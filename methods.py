

value2 = 654494965
value1 = 123456789
def send(data=0, value=40):
    '''
    This is the help description of send() method.
    IN: Integer
    OUT: Will return the data + 4.
    '''
    return data + 4 + value


def variable_argument_length(*args):
    print(args)
    return sum(args)


def test_variable_argument_length():
    print(variable_argument_length(12,3,4,4,4,4,4,8,9,8,8))


def variable_argument_length2(**kwargs):
    print(kwargs)


def test_variable_argument_length2():
    print(variable_argument_length2( first='one', second='two'))

def test_scope():
    value1 = (1, 2, 3, 4)
    value2 = 77777
    print(value2)
    for each_item in value1:

        print(each_item)
        print(value1)
    print(value2)





