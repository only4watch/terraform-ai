import hcl2

def parse_tf_file(path: str):
    with open(path, "r") as file:
        return hcl2.load(file)


def read_tf_as_text(path: str):
    with open(path, "r") as file:
        return file.read()
