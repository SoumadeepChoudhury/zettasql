import subprocess
import platform
import os
import random
if not os.path.exists(".NULL"):
    os.mkdir(".NULL")
PID = 0
process=None
PORT = str(random.randint(0,65336))
if not os.path.exists("./.log"):
    try:
        if platform.system() in ("Darwin","Linux"):
            process=subprocess.Popen(["python3","-m","http.server",PORT,"--directory",".NULL"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            PID =process.pid
        elif platform.system() == 'Windows':
            with open(os.devnull,'w') as nullVal:
                process=subprocess.Popen(["python", "-m", "http.server",PORT,"--directory",".NULL"],stdout=nullVal,stderr=nullVal)
                PID =process.pid
    except Exception as e:
        print(f"Error {e.args[0]}. Unable to connect to ZettaSQL serer.")

    if PID != 0:
        with open(".log",'wb') as file:
            import pickle
            try:
                data=str(PID)+"%"+str(PORT)
                pickle.dump(data,file)
            except:
                print('Unable to connect to ZettaSQL server.')
                process.terminate()
else:
    print("ZettaSQL server is already on.")
    
