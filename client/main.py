def main():
    try:
        from getpass import getpass
        import sys
        import os
        import signal
        def signal_control(SignalNumber, Frame):
            # function that controls the key events :- CTRL+C
            print("\n\nzettasql> ",end='')
        signal.signal(signal.SIGINT, signal_control) # handling singal event from keyboard.
        with open('info.log','r+') as file:
            # info.log file contains application information
            # checks for connection id and edits the info.log file for new connection id
            items=file.readlines()
            present=False
            file.seek(0)
            data=file.read()
            if "id :" not in data:
                _id=1
            else:
                present=True
                _id=int(str([i.split(":")[1].strip() for i in items if "id :" in i][0]))  # finding the location of "id :" and getting the value from that by splicing.
            file.seek(0)
            if not present:
                file.write(data+"id : "+str(_id+1)) # rewriting new data with connection id
            else:
                file.write(data.replace(str(f"id : {_id}"),str(f"id : {_id+1}"))) # updating the connection id
            version=str([i for i in items if "version :" in i][0]).split(":")[1].strip() # fetching the version code
        arg=sys.argv # getting the command line tags
        if len(arg)>=4 and arg[1]=='-u' and arg[3]=='-p':
            # checking for login criteria
            if os.path.exists("../server/.config"):
                # .config files stores users data like username and password.
                with open("../server/.config",'rb') as file:
                    import pickle
                    data=pickle.load(file)
                if data['username@admin']!=arg[2]:
                    print(f"Access Denied for {arg[2]} :- Not registered user.")
                    sys.exit()
            else:
                print(f"Access Denied for {arg[2]} :- Not registered user.")
                sys.exit()
            pas=getpass("Password: ")
            if data['password@admin'] != pas :
                print(f"Access Denied for {arg[2]} (with password : YES) ")
                sys.exit()
            else:
                if not os.path.exists("../server/.log"):
                    # .log file contains server information like it's state of connection
                    print("Error 1000 : Can't connect to ZettaSQL server")
                    sys.exit()
                print(f"Welcome to the ZettaSQL monitor.  Commands end with ; or \g.\nYour ZettaSQL connection id is {_id} \nZettaSQL Server version: {version} Ahens | An Initiative to Initial. \n \nCopyright (c) 2023, Ahens | An Initiative to Initial and/or its affiliates. \n\nAhens | An Initiative to Initial is a registered trademark of Ahens | An Initiative to Initial Corporation and/or its \n affiliates. Other names may be trademarks of their respective owners.\n\nType 'help;' or '\h' for help. Type '\c' to clear the current input statement.")
                while True:
                    cmd=input("\nzettasql> ")
                    if(cmd.lower() in ('exit','quit','bye')):
                        print('Bye')
                        break
                    else:
                        print(cmd)

        else:
            print("Access denied.")
            sys.exit()
    except:
        sys.exit()

if __name__=="__main__":            
    main()

