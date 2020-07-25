def readDomains(path):
    with open(path, 'r') as file:
        reader = file.read().split('\n')
        result = []
        for i in reader:
            i = i.strip()
            if i != '':
                result.append(i)
    return result


def writeLine(name, string):
    with open(name, 'a', encoding='utf8') as file:
        file.write(str(string) + '\n')

def writeLines(name, strings):
    with open(name, 'a', encoding='utf8') as file:
        for i in strings:
            file.write(str(i) + '\n')