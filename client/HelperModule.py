def parser(file: object, handle: str) -> list:
    while True:
        content = file.readLine().split('=')
        if handle.lower() == content[0].lower():
            data = content[1]
            break
    return data


def displayTable(field: list = None, records: list = None, sep: str = None):
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
                if sep != None:
                    print(
                        f"{records[i-1][j].replace(sep,''):^{maxLength[j]}}|", end='')
                else:
                    print(
                        f"{records[i-1][j]:^{maxLength[j]}}|", end='')
        print()
        if i == 0 or i == len(records):
            print(outliner)
    print(f"{len(records)} rows in set ", end='')


def validParenthesis(userInput: str):
    if "{" in userInput or "}" in userInput or '[' in userInput or ']' in userInput:
        return False
    listStack = []
    res = True
    for i in userInput:
        if i in '(':
            listStack.append(i)
        if i in ')':
            if '(' in listStack:
                listStack.pop()
                break
            else:
                res = False
                break
    if listStack == [] and len(userInput) >= 2 and res:
        return True
    return False


def isValidEntry(entry: str, datatype: str, length: int = None):
    pass


def getData(file: object):
    file = open("./databases/test.zdb", 'rb')
    data = []
    import pickle
    file.seek(0)
    while True:
        try:
            data.append(str(pickle.load(file)))
        except:
            break
    return data


def time(inner_func):
    import time

    def wrapped_func(*args, **kwargs):
        start = time.time()
        inner_func(*args, **kwargs)
        end = time.time()
        duration_secs = end - start
        # print(f"Executed {inner_func.__name__} in {duration_secs: .3f} secs")
        return round(duration_secs, 3)
    return wrapped_func


def checkForDefaultToken(tokens: list, re: object):
    try:
        present = list(filter(re.compile("default*").match, tokens))[0].strip()
        if re.fullmatch(r"^default\s?=\s?[0-9A-Za-z]+$", present) and present != "":
            defaultValue = present.split("=")[1].strip()
            if defaultValue != None:
                return True, defaultValue
        return True, None
    except:
        return False


def getConstraints(tokens: list, constraints: tuple):
    allConstraint: list = []
    # defaultPresent: bool = False
    for constraint in constraints:
        # if 'default' in constraint:
        # defaultPresent = True
        if tokens.count(constraint) == 1:
            allConstraint.append(constraint)
    allConstraint = ','.join(allConstraint)
    return allConstraint


def ifMultipleDatatype(tokens: list, datatype: list):
    count: int = 0
    for token in tokens:
        if 'default' in token:
            token = 'default'
        if datatype.count(token) == 1:
            count += 1
    if count > 1:
        return True
    return False


def getLength(tokens: list, datatypes: dict):
    if len(tokens) > 2:
        if tokens[1] in datatypes and int(tokens[2]) in range(*datatypes[tokens[1]]):
            return int(tokens[2])
    return None
