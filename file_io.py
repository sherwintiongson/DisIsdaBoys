from pathlib import Path


def test_pathlib():
    root = Path.cwd()
    print(root)


def test_file_read():
    root = (Path.cwd())
    root = (str(root) + "\\")
    keyfile = open(root + "test.txt", mode="r")
    keyfile.seek(0)
    file_content = keyfile.read()
    keyfile.close()
    return file_content


def test_file_write():
    root = Path.cwd()
    root = str(root) + "\\"
    keyfile = open(root + "test.txt", mode="w")
    keyfile.writelines("\n lora,")
    keyfile.writelines("\n lora1,")
    keyfile.writelines("\n lora2,")
    keyfile.writelines("\n lora3,")
    keyfile.writelines("\n lora4,")
    keyfile.close()

