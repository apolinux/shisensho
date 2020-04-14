import time
from configShisen import configShisen
class log:
    
    def save(text):
        logfile = configShisen.load('logfile')
        
        if not logfile:
            return
        
        logfile = configShisen.loadFile('logfile')
        
        with open(logfile, 'a') as f:
            line = "{}|{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),text)
            f.write(line)
        f.closed