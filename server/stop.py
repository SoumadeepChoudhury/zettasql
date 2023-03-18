def stop():
    import signal
    import subprocess
    import platform
    import os
    PID = 0
    if os.path.exists("./server/.log"):
        # .log contains server information
        with open("./server/.log", 'rb') as file:
            # loading data from file
            import pickle
            try:
                PID = int(str(pickle.load(file)).split("%")[0])
                if platform.system() != 'Windows':
                    # Stopping server process in Linux Based OS
                    os.kill(PID, signal.SIGKILL)
                else:
                    # Stopping server process in windows
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(PID)],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                file.close()
                # removing the file for new generation later.
                os.remove("./server/.log")
                try:
                    with open("./client/info.log", 'r+') as file:
                        # updating session information in info.log file which stores application state.
                        data = ''.join(file.readlines()[:-1])
                        file.truncate(0)
                        file.write(data)
                except:
                    pass
            except:
                print("Unable to stop ZettaSQL server.")
    else:
        print("ZettaSQL server is already stopped.")


if __name__ == "__main__":
    stop()
