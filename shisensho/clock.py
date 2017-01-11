import time
import math

class clock:
    
    def __init__(self):
        self.pause_clock = None
        self.initial_time = None
        self.last_diff = None

    def reset(self):
        self.initial_time = time.time()
        self.last_diff = 0
    
    def update(self):
        """
        updates the clock 
        if is paused the diff is fixed
        if is moving, the initial_time is fixed
        """
        if self.pause_clock:
            self.initial_time = time.time() - self.last_diff
            diff_t = self.last_diff
        else:    
            diff_t = time.time() - self.initial_time
            self.last_diff = diff_t
            
        diff = math.ceil(diff_t)
        return self.secondsToHms(diff)
    
    def secondsToHms(self,seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(h, m, s)
