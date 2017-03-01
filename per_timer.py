import time
import sched
import threading

# s = sched.scheduler(time.time, time.sleep)


class TimeTry:
    def __init__(self):
        self._t = None
        self._inx = 0

    def its_time(self):
        print "yhhhhoooooo", time.time()
        # s.enter(5, 1, its_time, ())
        # s.run()
        self._inx += 1
        self._t = threading.Timer(5, self.its_time, ())
        self._t.start()

    def timer_try(self):
        print time.time()
        # s.enter(5, 1, its_time, ())
        # s.run()
        self._t = threading.Timer(5, self.its_time, ())
        self._t.start()
        print "end", time.time()

    def run(self):
        self.timer_try()
        while True:
            print "@@@@@@"
            if self._inx == 10:
                self._t.cancel()
            time.sleep(3)

t = TimeTry()
t.run()

