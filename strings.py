""" dummy doc string """
import time as my_time


def basics_strings():
    """ dummy doc string """
    local_string = "Ocean's 13, Ocean's 14 and 15"
    print(local_string)
    print(local_string[5])


def reverse_indexing():
    """ dummy doc string """
    local_string = "123456789123456789t"
    print(local_string)
    print(local_string[-1])
    print(local_string[0:10:3])


def slicing():
    """ dummy doc string """
    local_string = "123456789123456789z"
    print(local_string[0:10:1])
    print(local_string[0:10:2])
    print(local_string[0:10:3])
    print(local_string[0:10:4])
    print(local_string[11:15:1])
    print(len(local_string))


def change_string_element():
    name = "Lora Samantha Tiongson"
    temp = name.split()
    print(temp)
    complete_name = temp[0] + " " + temp[1] + " Batislaon " + temp[2]
    print(complete_name)
    print(complete_name * 3)


def string_formatting():
    name = "my age is"
    print("my age is {2}, {1}, {0}".format("40", "41", "42"))


def float_formatting():
    my_float = 10000/777
    print("{:.5f}".format(my_float))


def hello_lora():
    """ dummy doc string """
    i = 0
    while True:
        i = i + 1
        my_time.sleep(2)
        print("elsa", i)
