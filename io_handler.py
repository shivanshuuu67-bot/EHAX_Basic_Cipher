import os


def read_text(text):

    return text


def read_file(filename):

    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def get_input(data):

    if os.path.isfile(data):
        return read_file(data)

    return read_text(data)

result = get_input("message.txt")

print(result)