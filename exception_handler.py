'''
Codes for experimenting exception handling in python
'''
from pathlib import Path


def test_simple_testing_exceptions():
    '''
    No exception example
    '''
    root = Path.cwd()
    root = str(root) + "\\"
    with open(root + "test.txt", mode="r", encoding="utf-8") as myfile:
        try:
            myfile.seek(0)
            file_content = myfile.read()
        except Exception:
            print("Error accessing file!")
        else:
            print("Everything seems to work well!")
        finally:
            myfile.close()
    print(type(file_content))
    print(file_content)
    print("end!!!")
    return file_content

def test_simple_testing_exceptions2():
    '''
    With exception example.
    '''
    cnt = 0
    result = 0
    while True:
        try:
            cnt = cnt + 1
            result = int(input("Please enter a number: " ))
        except:
            print("That is not a number. Please try again")
            continue
        else:
            print("Good number!!")
            break
        finally:
            print("Loop count = ", cnt)

    print("You entered number ", result)
