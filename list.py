""" dummy doc string """


def test_list():
    lista = ["one", "two", "three"]
    listb = ["four", "five"]
    list_all = lista + listb
    print(list_all)
    for x in list_all:
        print(x)
    list_all.reverse()
    for x in list_all:
        print(x.capitalize())
    list_all.reverse()
    list_all.pop()
    print("\n")
    for x in list_all:
        print(x.capitalize())

    print("\n")
    list_all.sort()
    for x in list_all:
        print(x.capitalize())

    print("\n")
    listc = [1, 2, 3, 4, 5]
    print(listc)
    listc.sort(reverse=True)
    print(listc)


