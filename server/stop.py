import signal
import os
PID=0
if os.path.exists("./log"):
    with open("log",'rb') as file:
        import pickle
        try:
            PID=pickle.load(file)
            os.kill(PID, signal.SIGKILL)
            os.remove("./log")
        except:
            print("Unable to stop ZettaSQL server.")
else:
    print("ZettaSQL server is already stopped.")
