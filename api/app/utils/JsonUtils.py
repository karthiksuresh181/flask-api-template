from json import dumps, load


def write_json(filename, data):
    json_object = dumps(data, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)


def read_json(path):
    with open(path) as json_file:
        data = load(json_file)
    return data
