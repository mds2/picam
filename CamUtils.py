import subprocess
import datetime
from os import path
import time

try: # by default we want our snapshots to come from the raspberry pi camera
    import picamera
    class Snapshotter:
        """Defines a class that allows us to take a snapshot to a filename
        very very thin wrapper around picamera.PiCamera
        only relevant method is "snap"
        """
        def __init__(self, w=1280, h=960, brightness=50):
            self.w = w
            self.h = h
            self.cam = picamera.PiCamera()
            if brightness:
                self.cam.brightness = brightness
        def snap(self, filename):
            self.cam.capture(filename, resize=(self.w, self.h))
except ImportError: # if that fails, use webcam
    class Snapshotter:
        """Fallback Snapshotter class that uses webcam over USB
        signature should match the Snapshotter we use when we use the built-in
        picamera
        """
        def __init__(self, w=640, h=480, brightness=100):
            if not brightness:
                brightness = 100
            self.args = ["fswebcam", "-r",
                         str(w) + "x" + str(h),
                         "--set", "brightness=" + str(brightness) + "%"]
        def snap(self, filename):
            p = subprocess.Popen(self.args + [filename])
            return p.wait()

class TimeStamp:
    def __init__(self):
        """Always initializes to NOW"""
        self.d = datetime.datetime.now()
    def sortable_string(self):
        """Gives a string suitable for use as a filename or database key,
        such that sorting a set of such strings lexicographically yields them
        in alphabetical order"""
        return "-".join([str(element) for element in self.d.timetuple()[:-3]])
    def display_string(self):
        return str(self.d)
    def datetime(self):
        return self.d

class TimedSnapshotter:
    """This packages up Snapshotter and TimeStamp into something
    that can take (and save) a labelled timestamped snapshot, either
    instantaneously, or after waiting for some interval after the last
    snapshot
    TODO : rename
    """
    def __init__(self, size=(640,480), interval=1.0, bright=None, dir="shots"):
        """ This class manages a webcam, keeps a simple webpage up to date,
        and also tries to make a webpage of thumbs
        """
        self.dir = dir
        self.snapper = Snapshotter(w=size[0], h=size[1], brightness=bright)
        self.interval = interval # interval between shots
        self.oldsnaps = []
        self.last_time = 0.0
    def dowork(self):
        t = TimeStamp()
        filename = path.join(self.dir, t.sortable_string() + ".jpg")
        self.snapper.snap(filename)
        return (t, filename)
    def work_and_wait(self):
        nexttime = self.last_time + self.interval
        self.last_time = time.time()
        time.sleep(max(0.0, nexttime - self.last_time))
        return self.dowork()

if __name__ == "__main__":
    w = TimedSnapshotter()
    w.dowork()
