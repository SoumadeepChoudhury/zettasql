def parser(file: object, handle: str) -> list:
    while True:
        content = file.readLine().split('=')
        if handle.lower() == content[0].lower():
            data = content[1]
            break
    return data


def displayTable(field: list = None, records: list = None):
    '''Display the output in tablular format'''
    maxLength = []  # To determine the maximum length/width of each field/column
    for i in range(len(field)):  # Finding maxlength for each fields
        length = len(field[i])
        for j in records:
            if length < len(str(j[i])):
                length = len(str(j[i]))
        maxLength.append(length+4)
    length = 0    # Designer the outliner shape - block
    outliner = ''
    while length < len(maxLength):
        outliner += f"+{'-'*maxLength[length]}"
        length += 1
    outliner += "+"
    for i in range(len(records)+1):  # Building Table format
        if i == 0:
            print(outliner)
        for j in range(len(maxLength)):
            if j == 0:
                print("|", end='')
            if i == 0:
                print(f"{field[j]:^{maxLength[j]}}|", end='')
            else:
                print(f"{records[i-1][j]:^{maxLength[j]}}|", end='')
        print()
        if i == 0 or i == len(records):
            print(outliner)
    print(f"{len(records)} rows in set\n")
