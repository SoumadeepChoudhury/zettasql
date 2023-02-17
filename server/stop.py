import signal
import subprocess
import platform
import os
PID=0
if os.path.exists("./.log"):
    with open(".log",'rb') as file:
        import pickle
        try:
            PID=int(str(pickle.load(file)).split("%")[0])
            if platform.system() != 'Windows':
                os.kill(PID, signal.SIGKILL)
            else:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(PID)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            file.close()
            os.remove("./.log")
        except:
            print("Unable to stop ZettaSQL server.")
else:
    print("ZettaSQL server is already stopped.")
