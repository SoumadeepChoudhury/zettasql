from HelperModule import *
import re
import os


FILE: object = None             # Holds the database file object
DATABASE_NAME: str = None       # Holds the database name
TABLE_DISPLAYED: bool = False   # Flag for if table is displayed
ERROR: bool = False             # Flag for any error
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
            FILE = open(f"./databases/{file}.zdb", 'rb+')
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
        if os.path.exists(f"./databases/{file}.zdb"):
            if not present:
                ERROR = True
                print(
                    f"ERROR 1021: Can't create database '{file}'; database exists")
        else:
            # Creates the file Instance (Temporary stored)
            _ = open(f"./databases/{file}.zdb", 'wb+')
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
        filesInDirectory: list = os.listdir("./databases/")
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
                            tokens, DATATYPES)
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
                        if tableName.lower() == names.split("=")[0].strip():
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
        print(tableData)
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


def desc(cmd):
    # TODO : display the outlayer or the table structure
    pass


def drop_database(cmd: str):
    # TODO : To delete the database from system
    pass


def drop_table(cmd: str):
    # TODO : To delete the table from database
    pass


def delete(cmd: str):
    # TODO : Delete records of the table without deleting the structure of the table.
    pass


COMMANDS: dict = {"use": use_Database, "create database": create_Database,
                  "show databases": show_Database, "show tables": show_Tables, "create table": create_Table, "desc": desc, "drop database": drop_database, "drop table": drop_table, "delete": delete}


@time
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
            if os.path.exists("../server/.config"):
                # .config files stores users data like username and password.
                with open("../server/.config", 'rb') as file:
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
                if not os.path.exists("../server/.log"):
                    # .log file contains server information like it's state of connection
                    print("ERROR 1000 : Can't connect to ZettaSQL server")
                    sys.exit()
                with open('info.log', 'r+') as file:
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
