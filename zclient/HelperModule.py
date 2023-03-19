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


def getData(file: object):
    data: list = []
    import pickle
    file.seek(0)
    while True:
        try:
            data.append(str(pickle.load(file)))
        except:
            break
    return data


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
    for constraint in constraints:
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


def getLength(tokens: list, datatypes: dict, constraints: tuple):
    if len(tokens) > 2:
        if tokens[2] in constraints:
            return datatypes[tokens[1]][1]
        if tokens[1] in datatypes and int(tokens[2]) in range(*datatypes[tokens[1]]):
            return int(tokens[2])
    return None


def getTableData(file: object, tableName: str):
    existingTable = getData(file)
    for table in existingTable:
        if table.startswith(tableName):
            return table
    return None


def isValidEntry(tableData: list, input: list):
    def checkLengthRange(inputLength: int, datatypeElement: str, datatype: str):
        if datatype in ('varchar', 'char', 'blob', 'int'):
            try:
                datatypeMaxRange: int = int(
                    datatypeElement[datatypeElement.rfind('(')+1:datatypeElement.find(")")])
                if inputLength-2 <= datatypeMaxRange:
                    return True
            except:
                return True
        return True
    validity: dict = {'int': 1, 'varchar': "", 'char': '',
                      'blob': '', 'date': '', 'decimal': 2.0, 'bool': True}
    if len(tableData) == len(input):
        for index in range(len(tableData)):
            datatype: str = tableData[index].split(",")[0]
            datatypeElement: str = datatype
            datatype = datatype[datatype.find("(")+1:datatype.rfind(")")]
            datatype = datatype.split("(")[0]
            if datatype == 'int' and input[index] == "''":
                input[index] = "null"
                continue
            if not type(eval(input[index])) == type(validity[datatype]) or not checkLengthRange(len(input[index]), datatypeElement, datatype):
                return False
    return True


def insertDefaultValue(keys: list, value: list, input: str):
    if 'default' in keys and input == "''":
        startIndex: int = keys.find("default(")+8
        endIndex: int = keys[startIndex:].find(")")+startIndex
        try:
            return eval(keys[startIndex:endIndex])
        except:
            return keys[startIndex:endIndex]
    if input == 'null':
        return input
    return eval(input)


def getIndexPos_selectedItems(data: list, items: list):
    newList_Item: dict = {}
    for item in items:
        for element in data:
            if element.startswith(item):
                newList_Item[item] = data.index(element)
    return newList_Item
