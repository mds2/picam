import CamUtil
import SimpleHTTPServer
import SocketServer

class Webcam:
    """Manages snapshots and launches a simple web server
    Does it in such a way that would never fly in a commercial
    web environemnt"""
    def __init__(self):
        self.snapper = TimedSnapshotter()
        self.
    def webcam_looponce(slef):
        (timestamp, filename) = self.snapper.work_and_wait()
        

    def RunWebcam

if __name__ == "__main__":
    def runwebserver():
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        port = 8000
        httpd = SocketServer.TCPServer(("", port), handler)
        print "serving at port " + str(port)
        httpd.serve_forever()
    import multiprocessing as mp
    p1 = mp.Process(target=runwebcam)
    p2 = mp.Process(target=runwebserver)
    p2.start()
    p1.start()
    p2.join()
    p1.join()

