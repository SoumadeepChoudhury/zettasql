import subprocess
import platform
import os
import random
import pickle
if not os.path.exists(".NULL"):
    os.mkdir(".NULL")
PID = 0
process=None
PORT = str(random.randint(0,65336))
if not os.path.exists("./.log"):
    # .log file contains the server information.
    try:
        if not os.path.exists("./.config"):
            # .config file contains the cloent details.
            with open("./.config",'wb') as file:
                # Upload the user credentials in .config
                from getpass import getpass
                print("[*] Create root User")
                username=input("[*] Enter root username: ")
                password=getpass("[*] Enter root password: ")
                pickle.dump({'username@admin':username,'password@admin':password},file)
        if platform.system() in ("Darwin","Linux"):
            # Starting the server in Linux Based OS
            process=subprocess.Popen(["python3","-m","http.server",PORT,"--directory",".NULL"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            PID = process.pid # Getting the PID in order to kill it later
        elif platform.system() == 'Windows':
            # Start server in Windows OS
            with open(os.devnull,'w') as nullVal:
                process=subprocess.Popen(["python", "-m", "http.server",PORT,"--directory",".NULL"],stdout=nullVal,stderr=nullVal)
                PID =process.pid
    except Exception as e:
        print(f"Error {e.args[0]}. Unable to connect to ZettaSQL serer.")

    if PID != 0:
        with open(".log",'wb') as file:
            try:
                # Updating server information in .log file
                data=str(PID)+"%"+str(PORT)
                pickle.dump(data,file)
            except:
                print('Unable to connect to ZettaSQL server.')
                process.terminate()
else:
    print("ZettaSQL server is already on.")
    
