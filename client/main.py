from .HelperModule import *
import re
import os


FILE: object = None             # Holds the database file object
DATABASE_NAME: str = None       # Holds the database name
TABLE_DISPLAYED: bool = False   # Flag for if table is displayed
ERROR: bool = False             # Flag for any error
# KEYS,EXTRAS -> Used in desc table for showing the structure
KEYS: list = ["primary_key", "foreign_key", "unique_key"]
EXTRAS: list = ["auto_increment"]
DATATYPES: dict = {'int': [0, 4294967295], 'varchar': [1, 256], 'blob': [0, 65535], 'char': [1, 256], 'date': [],
                   'decimal': [], 'bool': []}  # Contains the datatypes
CONSTRAINTS = ('auto_increment', 'primary_key',
               'unique_key', 'foreign key', 'default')

DATATYPE_CONSTRAINT_MATCH: dict = {'int': ['primary_key', 'auto_increment', 'foreign_key', 'unique_key', 'deafult'],
                                   'varchar': ['default', 'primary_key', 'foreign_key', 'unique_key'],
                                   'char': ['default', 'primary_key', 'foreign_key', 'unique_key'],
                                   'blob': ['default', 'primary_key', 'foreign_key', 'unique_key'],
                                   'date': ['default', 'primary_key', 'foreign_key', 'unique_key'],
                                   'decimal': ['default', 'primary_key', 'foreign_key', 'unique_key', 'auto_increment'],
                                   'bool': ['default']}
# NOTE : the records should be in row wise per list Eg -> [[row1 details],[row2 details]...]


def use_Database(cmd: str):
    global ERROR
    if re.fullmatch(r"^use (\S*);$", cmd):
        file: str = cmd.replace("use ", "").strip().replace(";", "").strip()
        global FILE, DATABASE_NAME
        try:
            # Globally opens the file for future use.
            FILE = open(f"./client/databases/{file}.zdb", 'rb+')
            DATABASE_NAME = file
        except FileNotFoundError:
            ERROR = True
            print(f"ERROR 1020: Unknown database '{file}' ")
    else:
        ERROR = True
        bug: list = re.split(r'^use (\S*);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL Commands near \'{bug[0].strip()}\'.")


def create_Database(cmd: str):
    present: bool = False
    global ERROR
    if re.fullmatch(r"^create database (\S*);$", cmd) or re.fullmatch(r"^create database if not exists ([\S]*);$", cmd):
        if "if not exists" in cmd:
            present = True
        # Getting the file (database) Name
        file: str = cmd.replace(";", "").strip().split()[-1]
        if os.path.exists(f"./client/databases/{file}.zdb"):
            if not present:
                ERROR = True
                print(
                    f"ERROR 1021: Can't create database '{file}'; database exists")
        else:
            # Creates the file Instance (Temporary stored)
            _ = open(f"./client/databases/{file}.zdb", 'wb+')
            _.close()
    else:
        ERROR = True
        bug: list = re.split(
            r'^create database (\S*);$' if not present else r'^create database if not exists (\S*);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def show_Database(cmd: str):
    global ERROR
    if re.fullmatch(r"^show databases;$", cmd):
        global TABLE_DISPLAYED
        files: list = list()
        filesInDirectory: list = os.listdir("./client/databases/")
        for i in filesInDirectory:
            if not i.startswith("."):
                files.append([i])
        displayTable(field=["Databases"], records=files, sep=".zdb")
        TABLE_DISPLAYED = True
    else:
        ERROR = True
        bug: list = re.split(r'^show databases;$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def show_Tables(cmd: str):
    global ERROR
    if re.fullmatch(r"^show tables;$", cmd):
        global FILE, TABLE_DISPLAYED
        if FILE == None:
            ERROR = True
            print("ERROR 1022 : ZettaSQL Database not selected.")
        else:
            import pickle
            FILE.seek(0)
            tables: list = []
            while True:
                try:
                    data = str(pickle.load(FILE)).split('=')[0].strip()
                    tables.append([data])
                except:
                    break
            displayTable(field=[
                f'Table_in_{DATABASE_NAME}'], records=tables)
            TABLE_DISPLAYED = True
    else:
        ERROR = True
        bug: list = re.split(r'^show tables;$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def create_Table(cmd: str):
    global ERROR, DATATYPES, CONSTRAINTS, FILE, DATATYPE_CONSTRAINT_MATCH
    if re.fullmatch(r"^create table (\w+\s?\((\S{1,}\s\S{1,},?\s*)+\));$", cmd):
        cmd = str(
            (cmd.replace("create table ", "").strip()).replace(";", ""))    # replacing unnnecessary strings
        items: list = cmd[
            cmd.find("(")+1:cmd.rfind(")")].split(",")  # getting the name,datatype and value of arguments passed
        tableName: str = cmd[:cmd.find(
            '(')].strip()     # Contain the table name
        tableData: str = f"{tableName}="+"{"
        for item in items:
            if re.fullmatch("^\S+\s\S+(\s*(\(?)([1-9][0-9]*)(\)?))?(\s?\S*)+$", item.strip()) and validParenthesis(item):
                # getting the names, datatypes and values from command in 'item'
                itemModified: str = re.sub("[\(\)]", " ", item).strip()
                tokens: list = itemModified.split(' ')
                # removing empty element from list of 'tokens' by list comprehension
                tokens = [i.strip() for i in tokens if i != '']
                if ifMultipleDatatype(tokens, list(DATATYPES.keys())):
                    ERROR = True
                    tableData = ""
                    print(
                        f"ERROR 1011: Syntax Error in ZettaSQL command near '{item}'")
                    break
                tableNameAlreadyExists: bool = False  # To check if table_name already exists
                if tokens[1] in DATATYPES:
                    name: str = tokens[0]
                    datatype: str = tokens[1]
                    try:
                        length: int | None = getLength(
                            tokens, DATATYPES, CONSTRAINTS)
                        constraints: str | list = getConstraints(
                            tokens, CONSTRAINTS)
                    except:
                        ERROR = True
                        tableData = ""
                        print(
                            f"ERROR 1011: Syntax Error in ZettaSQL command near '{item}'")
                        break
                    defaultValue: int | float | str | bool | None = None
                    defaultPresent: bool = checkForDefaultToken(tokens, re)
                    if defaultPresent:
                        # default value entered might be of wrong type
                        try:
                            # If default value is not given
                            if defaultPresent[1] == None:
                                raise
                            if datatype not in ('varchar', 'char', 'date'):
                                defaultValue = eval(defaultPresent[1])
                            else:
                                defaultValue = defaultPresent[1]
                            constraints += f',default({defaultValue})' if constraints != '' else f'default({defaultValue})'
                        except:
                            ERROR = True
                            tableData = ""
                            print(
                                f"ERROR 1024: Value error in default constraint near default={defaultPresent[1]}")
                            break
                    data = getData(FILE)
                    for names in data:          # Checking for if tableName exists
                        if tableName.lower() == names.split("=")[0].strip().lower():
                            tableData = ""
                            print(
                                f"ERROR 1023: Cannot create table. '{tableName}' already exists.")
                            tableNameAlreadyExists = True
                            ERROR = True
                            break
                    if tableNameAlreadyExists:
                        break
                    # Format of table --> Table_Name={"col_name(datatype,constrainst)":[...],"col_name(datatype,constraint)":[...]}
                    tableData += f"\"{name}({datatype}{'('+str(length)+')' if length!=None else ''}{(','+constraints) if constraints!='' else ''})\":[]{',' if item!=items[-1] else ''}"
                else:
                    ERROR = True
                    tableData = ""
                    print(
                        f"ERROR 1011: Syntax Error in ZettaSQL command near '{tokens[1]}'")
                    break
            else:
                ERROR = True
                tableData = ""
                print(
                    f"ERROR 1011: Syntax Error in ZettaSQL command near '{item}'")
                break
        tableData += '}' if tableData != "" else ''
        if FILE != None and tableData != "":
            import pickle
            FILE.seek(0)
            for i in data:
                pickle.dump(i, FILE)
            pickle.dump(tableData, FILE)
            FILE.flush()
    else:
        ERROR = True
        bug: list = re.split(r'^create table (\S*)\(\S* \S*\);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def desc(cmd: str):
    global ERROR, TABLE_DISPLAYED, FILE, DATATYPES
    if re.fullmatch(r"^desc (\S+)\s?;$", cmd):
        cmd = cmd[:-1]
        preset: list = None
        try:
            cmd = cmd.split(" ")[1].strip()
            existingTables: list = getData(FILE)
            for tableName in existingTables:
                if cmd.lower() == tableName.split("=")[0].strip().lower():
                    preset: dict = eval(tableName.split("=")[1].strip())
                    break
            if preset == None:
                ERROR = True
                print(f"ERROR 1019: Unknown table '{cmd}'")
            else:
                fields: list = ["Field", "Type",
                                "Null", "Key", "Default", "Extra"]
                records: list = []
                added: bool = False
                for key in preset.keys():
                    dataPreset: list = [key[:key.find("(")]]
                    defaultPresent: bool = False
                    key = key[key.find('(')+1:key.rfind(')')]
                    keyElements = key.split(",")
                    for element in keyElements:
                        field = re.split("[\(\)]", element)
                        fieldName = field[0]
                        if 'default' in field:
                            defaultPresent = True
                            break
                        if len(field) > 1:
                            if int(field[1]) == DATATYPES[fieldName][1]:
                                dataPreset.append(fieldName)
                            else:
                                dataPreset.append(f"{fieldName}({field[1]})")
                                added = True
                    if fieldName in DATATYPES and not added:
                        dataPreset.append(fieldName)
                    if defaultPresent:
                        default = field[1]
                    extras = list(set(EXTRAS) & set(keyElements))
                    if extras == []:
                        extras = ''
                    specialKey = list(set(KEYS) & set(keyElements))
                    if specialKey == []:
                        specialKey = ''

                    dataPreset.extend([
                        'no' if specialKey != '' else 'yes', specialKey[0][0:3] if specialKey != '' else '', default if defaultPresent else "null", extras[0] if extras != '' else ''])
                    records.append(dataPreset)
                displayTable(field=fields, records=records)
                TABLE_DISPLAYED = True

        except:
            ERROR = True
            bug: list = re.split(r'^desc (\S+);$', cmd)
            print(
                f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")
    else:
        ERROR = True
        bug: list = re.split(r'^desc (\S+);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def drop_database(cmd: str):
    global ERROR, FILE
    if re.fullmatch(r"^drop database (\S+);$", cmd):
        file = re.split(r"^drop database (\S+);$", cmd)[1]
        if os.path.exists(f"./client/databases/{file}.zdb"):
            os.remove(f"./client/databases/{file}.zdb")
            FILE_name: str = str(FILE.name)
            if file == FILE_name[FILE_name.rfind("/")+1:FILE_name.rfind(".")]:
                FILE = None
        else:
            ERROR = True
            print(f"ERROR 1020: Unknown database '{file}'")
    else:
        ERROR = True
        bug: list = re.split(r'^drop database (\S+);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def drop_table(cmd: str):
    global ERROR, FILE
    if re.fullmatch(r"^drop table (\S+);$", cmd):
        existingTables: list = getData(FILE)
        tableName: str = re.split(r"^drop table (\S+);$", cmd)[1].strip()
        tableFound: bool = False
        import pickle
        FILE.seek(0)
        FILE.truncate(0)
        for table in existingTables:
            if table.startswith(f"{tableName}="):
                tableFound = True
                continue
            pickle.dump(table, FILE)
        FILE.flush()
        if not tableFound:
            ERROR = True
            print(f"ERROR 1019: Unknown table '{tableName}'")
    else:
        ERROR = True
        bug: list = re.split(r'^drop table (\S+);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def delete(cmd: str):
    global ERROR, FILE
    if re.fullmatch(r"^delete from table (\S+);$", cmd):
        existingTables: list = getData(FILE)
        tableName: str = re.split(r"^delete from table (\S+);$", cmd)[1]
        tableFound: bool = False
        import pickle
        FILE.seek(0)
        for table in existingTables:
            if table.startswith(f"{tableName}="):
                tableFound = True
                table = eval(table.split("=")[1].strip())
                table = {x: [] for x in table}
                table = tableName+'='+str(table)
            pickle.dump(table, FILE)
        FILE.flush()
        if not tableFound:
            ERROR = True
            print(f"ERROR 1019: Unknown table '{tableName}'")
    else:
        ERROR = True
        bug: list = re.split(r'^delete from table (\S+);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def insert(cmd: str):
    global ERROR, FILE
    # insert into table2(no,sname) values(1,"Hi Hello");
    if re.fullmatch(r"^insert into (\S+)\svalues\s?\(\S+\);$", cmd):
        tableName = re.split(
            r"^insert into (\S+)\svalues\s?\(\S+\);$", cmd)[1].strip().lower()
        cmd = cmd[:-1].strip()  # removing the semicolon
        cmd = cmd[cmd.rfind("(")+1:cmd.rfind(")")]  # getting the values
        cmd = cmd.split(",")            # splitting the values
        refinedInput = [i for i in cmd if i != '']   # removing blank spaces
        tableData: str = eval(getTableData(
            FILE, tableName).split("=")[1].strip())
        try:
            if len(list(tableData.keys())) == len(refinedInput) and isValidEntry(list(tableData.keys()), refinedInput):
                index = 0
                for key, value in tableData.items():
                    refinedInput[index] = insertDefaultValue(
                        key, value, refinedInput[index])
                    if refinedInput[index] == '' or refinedInput[index] == "''":
                        refinedInput[index] = 'null'
                    value.append(refinedInput[index])
                    index += 1
                if FILE != None:
                    existingTables: list = getData(FILE)
                    import pickle
                    FILE.seek(0)
                    for table in existingTables:
                        if not table.startswith(tableName):
                            pickle.dump(table, FILE)
                            continue
                        pickle.dump(f"{tableName}={tableData}", FILE)
                    FILE.flush()
            else:
                raise ValueError("Entry doesn't satisfy")
        except Exception as e:
            ERROR = True
            print(
                f"ERROR 1011: Syntax Error in ZettaSQL command. \"{e}\"")
        if tableData == None:
            ERROR = True
            print(f"ERROR 1019: Unknown Table '{tableName}'")
    else:
        ERROR = True
        bug: list = re.split(r"^insert into (\S+)\svalues\s?\(\S+\);$", cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


def select(cmd: str):
    global ERROR, FILE, TABLE_DISPLAYED
    if re.fullmatch(r"^select [\*|(\S+\s?,?\s?)*]+ from \S+;$", cmd):
        cmd = cmd[:-1]
        cmd = cmd.split(" ")
        items: list = cmd[cmd.index("select")+1:cmd.index("from")]
        items = items[0].split(",") if len(items) == 1 else items
        items = [x.replace(",", "").strip()
                 for x in items if x.strip() not in (",", "", " ")]
        tableName: str = cmd[-1]
        if '*' in items and len(items) > 1:
            ERROR = True
            print(
                f"ERROR 1011: Syntax Error in ZettaSQL command near \'{items[1]}\'")
            return
        data: dict = eval(getTableData(FILE, tableName).split("=")[1].strip())
        fields: list = []
        records: list = []
        for keys in data.keys():
            fields.append(keys[:keys.find("(")])
        if '*' in items:
            for times in range(len(list(data.values())[0])):
                recordLine: list = []
                for values in data.values():
                    # print(times, "-->", values[times])
                    recordLine.append(values[times])
                records.append(recordLine)
            displayTable(field=fields, records=records)
            TABLE_DISPLAYED = True
        else:
            updateField: list = []
            for item in items:
                if item in fields:
                    updateField.append(item)
                else:
                    ERROR = True
                    print(
                        f"ERROR 1011: Syntax Error in ZettaSQL command near '{item}'")
                    return
            fields = updateField
            itemIndexed: dict = getIndexPos_selectedItems(
                list(data.keys()), items)
            for times in range(len(list(data.values())[0])):
                recordLine: list = []
                for itemIndex in itemIndexed.values():
                    recordLine.append(list(data.values())[itemIndex][times])
                records.append(recordLine)
            displayTable(field=fields, records=records)
            TABLE_DISPLAYED = True

    else:
        ERROR = True
        bug: list = re.split(
            r"^select [\s?\*\s?|(\S+\s?,?\s?)*]+ from \S+;$", cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


COMMANDS: dict = {"use": use_Database, "create database": create_Database,
                  "show databases": show_Database, "show tables": show_Tables, "create table": create_Table, "desc": desc, "drop database": drop_database, "drop table": drop_table, "delete from": delete, "insert into": insert, "select": select}


def main():
    try:
        from getpass import getpass
        import sys
        import signal
        import readline

        global TABLE_DISPLAYED, COMMANDS, ERROR

        flag: bool = False

        def signal_control(SignalNumber: object, Frame: object):
            # global flag
            # function that controls the key events :- CTRL+C
            if flag:
                print("\n\nzettasql> ", end='')
            else:
                print("\rPassword: ", end='')
        # handling singal event from keyboard.
        signal.signal(signal.SIGINT, signal_control)

        arg: list = sys.argv  # getting the command line tags
        if len(arg) >= 4 and arg[1] == '-u' and arg[3] == '-p':
            # checking for login criteria
            if os.path.exists("./server/.config"):
                # .config files stores users data like username and password.
                with open("./server/.config", 'rb') as file:
                    import pickle
                    data: dict = pickle.load(file)
                if data['username@admin'] != arg[2]:
                    print(
                        f"Access Denied for {arg[2]} :- Not registered user.")
                    sys.exit()
            else:
                print(f"Access Denied for {arg[2]} :- Not registered user.")
                sys.exit()
            pas: str = getpass("Password: ")
            if data['password@admin'] != pas:
                print(f"Access Denied for {arg[2]} (with password : YES) ")
                sys.exit()
            else:
                flag = True
                if not os.path.exists("./server/.log"):
                    # .log file contains server information like it's state of connection
                    print("ERROR 1000 : Can't connect to ZettaSQL server")
                    sys.exit()
                with open('./client/info.log', 'r+') as file:
                    # info.log file contains application information
                    # checks for connection id and edits the info.log file for new connection id
                    items: list = file.readlines()
                    present: bool = False
                    file.seek(0)
                    data: str = file.read()
                    if "id :" not in data:
                        _id: int = 1
                    else:
                        present = True
                        # finding the location of "id :" and getting the value from that by splicing.
                        _id = int(str([i.split(":")[1].strip()
                                       for i in items if "id :" in i][0]))
                    file.seek(0)
                    if not present:
                        # rewriting new data with connection id
                        file.write(data+"id : "+str(_id+1))
                    else:
                        # updating the connection id
                        file.write(data.replace(
                            str(f"id : {_id}"), str(f"id : {_id+1}")))
                    version: int | float = str([i for i in items if "version :" in i][0]).split(
                        ":")[1].strip()  # fetching the version code
                print("""
 ______     _   _        _____  _____ _
|___  /    | | | |      /  ___||  _  | |
   / /  ___| |_| |_ __ _\ `--. | | | | |
  / /  / _ \ __| __/ _` |`--. \| | | | |
./ /__|  __/ |_| || (_| /\__/ /\ \/' / |____
\_____/\___|\__|\__\__,_\____/  \_/\_\_____/
    """)
                print(f"Welcome to the ZettaSQL monitor.  Commands end with ; or \g.\nYour ZettaSQL connection id is {_id} \nZettaSQL Server version: {version} Ahens | An Initiative to Initial. \n \nCopyright (c) 2023, Ahens | An Initiative to Initial and/or its affiliates. \n\nAhens | An Initiative to Initial is a registered trademark of Ahens | An Initiative to Initial Corporation and/or its \n affiliates. Other names may be trademarks of their respective owners.\n\nType 'help;' or '\h' for help. Type '\c' to clear the current input statement.")
                import time
                while True:
                    ERROR = False
                    cmd: str = input("\nzettasql> ").lower()
                    if cmd == "":
                        continue
                    if cmd[-1] != ';':
                        print(
                            f"ERROR 1011: Syntax Error in ZettaSQL command near '{cmd[-5:]}'")
                        continue
                    if (cmd in ('exit;', 'quit;', 'bye;')):
                        global FILE
                        # Close the FILE (database) instance.
                        FILE.close() if FILE != None else True
                        print('Bye')
                        break
                    else:
                        try:
                            for item in COMMANDS.keys():
                                if item in cmd:
                                    # Calling respective functions
                                    start: float = time.time()  # Getting execution time
                                    COMMANDS[item](cmd)
                                    end: float = time.time()
                                    if not ERROR:
                                        if TABLE_DISPLAYED:
                                            print(
                                                f"({round((end-start),3)} sec)")
                                            TABLE_DISPLAYED = False
                                        else:
                                            print(
                                                f"Query ran in {round((end-start),3)} sec.")
                                    break
                            else:
                                print(
                                    f"ERROR 1012: Unknown ZettaSQL command : '{cmd.split()[0]}'")
                        except:
                            pass

        else:
            print("Access denied.")
            sys.exit()
    except:
        sys.exit()


if __name__ == "__main__":
    main()
