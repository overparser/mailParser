def read_lines(path):
    with open(path, 'r') as file:
        reader = file.read().split('\n')
        result = []
        for i in reader:
            i = i.strip()
            if i != '':
                result.append(i)
    return result


def cutDomains(path, count):
    reader = read_lines(path)
    writeLines(path, reader[count:], 'w')
    return reader[:count]


def writeLine(name, string, mod='a'):
    with open(name, mod, encoding='utf8') as file:
        file.write(str(string) + '\n')

def writeLines(name, strings, mod='a'):
    with open(name, mod, encoding='utf8') as file:
        for i in strings:
            file.write(str(i) + '\n')