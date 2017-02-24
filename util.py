import os


def write_file(filename, contents):
    (dirname, _) = os.path.split(filename)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(contents)
