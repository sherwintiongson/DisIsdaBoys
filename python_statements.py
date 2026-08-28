


def test_statements():
    if 3 == 2:
        print("yes.. 3 is 3")
    elif 6 == 6:
        print("6 is 6")
    else:
        print("no.. 3 is not 2")

def test_switch(mykey):
    match mykey:
        case 1:
            print("key is ", mykey)
        case 2:
            print("key is ", mykey)
        case other:
            print("other")


def test_for_loop():
    mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(len(mylist))
    for each_element in mylist:
        if 0 == (each_element % 2):
            print("Even: ", each_element)
        else:
            print("Odd: ", each_element)


def test_while_loop():
    mylist = mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(mylist)
    i = 0
    while (i<len(mylist)):
        print("\r ", mylist[i])
        i = i + 1
    else:
        print("End of list.")


def test_pass():
    pass


def test_continue():
    mylist = mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(mylist)
    for each_element in mylist:
        if 8 == each_element:
            # skip printing if 8
            continue
        print(each_element)

def test_break():
    mylist = mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(mylist)
    for each_element in mylist:
        # stop printing when more than 7
        if(each_element > 7):
            break
        print(each_element)







