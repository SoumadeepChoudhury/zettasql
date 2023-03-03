from HelperModule import *
import re
import readline

FILE = None


def use_Database(cmd):
    if re.fullmatch(r"^use database ([\S]*);$", cmd):
        file = cmd.replace("use database", "").strip().replace(";", "").strip()
        global FILE
        try:
            # Globally opens the file for future use.
            FILE = open(f"./databases/{file}.zdb", 'r+')
        except FileNotFoundError:
            print(f"ERROR 1020: Unknown database '{file}' ")
    else:
        bug = re.split(r'^use database ([\S]*);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL Commands near \'{bug[0].strip()}\'.")


def create_Database(cmd):
    present = False
    if re.fullmatch(r"^create database ([\S]*);$", cmd) or re.fullmatch(r"^create database if not exists ([\S]*);$", cmd):
        if "if not exists" in cmd:
            present = True
        # cmd = cmd.replace(";", "").strip().split()
        # Getting the file (database) Name
        file = cmd.replace(";", "").strip().split()[-1]
        import os
        if os.path.exists(f"./databases/{file}.zdb"):
            if not present:
                print(
                    f"ERROR 1021: Can't create database '{file}'; database exists")
        else:
            # Creates the file Instance (Temporary stored)
            _ = open(f"./databases/{file}.zdb", 'w+')
            _.close()
    else:
        bug = re.split(
            r'^create database ([\S]*);$' if not present else r'^create database if not exists ([\S]*);$', cmd)
        print(
            f"ERROR 1011: Syntax Error in ZettaSQL command near \'{bug[len(bug)//2]}\'")


COMMANDS = {"use": use_Database, "create database": create_Database}


def main():
    try:
        from getpass import getpass
        import sys
        import os
        import signal
        flag = False

        def signal_control(SignalNumber, Frame):
            # global flag
            # function that controls the key events :- CTRL+C
            if flag:
                print("\n\nzettasql> ", end='')
            else:
                print("\rPassword: ", end='')
        # handling singal event from keyboard.
        signal.signal(signal.SIGINT, signal_control)
        with open('info.log', 'r+') as file:
            # info.log file contains application information
            # checks for connection id and edits the info.log file for new connection id
            items = file.readlines()
            present = False
            file.seek(0)
            data = file.read()
            if "id :" not in data:
                _id = 1
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
            version = str([i for i in items if "version :" in i][0]).split(
                ":")[1].strip()  # fetching the version code
        arg = sys.argv  # getting the command line tags
        if len(arg) >= 4 and arg[1] == '-u' and arg[3] == '-p':
            # checking for login criteria
            if os.path.exists("../server/.config"):
                # .config files stores users data like username and password.
                with open("../server/.config", 'rb') as file:
                    import pickle
                    data = pickle.load(file)
                if data['username@admin'] != arg[2]:
                    print(
                        f"Access Denied for {arg[2]} :- Not registered user.")
                    sys.exit()
            else:
                print(f"Access Denied for {arg[2]} :- Not registered user.")
                sys.exit()
            pas = getpass("Password: ")
            if data['password@admin'] != pas:
                print(f"Access Denied for {arg[2]} (with password : YES) ")
                sys.exit()
            else:
                flag = True
                if not os.path.exists("../server/.log"):
                    # .log file contains server information like it's state of connection
                    print("ERROR 1000 : Can't connect to ZettaSQL server")
                    sys.exit()
                print("""
 ______     _   _        _____  _____ _     
|___  /    | | | |      /  ___||  _  | |    
   / /  ___| |_| |_ __ _\ `--. | | | | |    
  / /  / _ \ __| __/ _` |`--. \| | | | |    
./ /__|  __/ |_| || (_| /\__/ /\ \/' / |____
\_____/\___|\__|\__\__,_\____/  \_/\_\_____/
    """)
                print(f"Welcome to the ZettaSQL monitor.  Commands end with ; or \g.\nYour ZettaSQL connection id is {_id} \nZettaSQL Server version: {version} Ahens | An Initiative to Initial. \n \nCopyright (c) 2023, Ahens | An Initiative to Initial and/or its affiliates. \n\nAhens | An Initiative to Initial is a registered trademark of Ahens | An Initiative to Initial Corporation and/or its \n affiliates. Other names may be trademarks of their respective owners.\n\nType 'help;' or '\h' for help. Type '\c' to clear the current input statement.")
                while True:
                    cmd = input("\nzettasql> ").lower()
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
                                    COMMANDS[item](cmd)
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
    # create_Database("test")
    # displayTable(field=["Name","ID","Phone"],records=[["Soumadeep Choudhury",12,23456],["Sneha Ganguly","156",45678]])
    # displayTable(field=["Name"],records=[["Soumadeep"]])
