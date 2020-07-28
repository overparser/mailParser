def read_lines(path):
    with open(path, 'r') as file:
        reader = file.read().split('\n')
        result = []
        for i in reader:
            i = i.strip()
            if i != '':
                result.append(i)
    return result


def cut_lines(path, count):
    reader = read_lines(path)
    write_lines(path, reader[count:], 'w')
    return reader[:count]


def write_line(path, string, mod='a'):
    with open(path, mod, encoding='utf8') as file:
        file.write(str(string) + '\n')


def write_lines(path, strings, mod='a'):
    strings = strings if type(strings) == list else [strings]

    with open(path, mod, encoding='utf8') as file:
        for i in strings:
            if i:
                file.write(str(i) + '\n')