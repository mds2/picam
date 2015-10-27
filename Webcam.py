import CamUtil
import SimpleHTTPServer
import SocketServer

def spew_simple_webpage(snaplist):
    outfile = open("index.html", "w")
    outfile.write("<html>\n")
    outfile.write("<head><title>Simple webcam v 0.2</title></head>\n")
    outfile.write("<body>\n")
    for (title, file) in snaplist.reverse():
        outfile.write("<br/><br/>\n<img src=\"" + file + "\"/>\n")
        outfile.write("<a href=\"" + file + "\">" + title + "</a>\n")
    outfile.write("<hr/>\n")
    outfile.write("<a href=\"shots\">shots</a>\n")
    outfile.write("</body></html>")

class Webcam:
    """Manages snapshots and launches a simple web server
    Does it in such a way that would never fly in a commercial
    web environemnt"""
    def __init__(self, maxsnaps=10, handlesnaps = spew_simple_webpage):
        self.snapper = TimedSnapshotter()
        self.snapnames = []
    def webcam_looponce(self):
        (timestamp, filename) = self.snapper.work_and_wait()
        self.snapnames.append((timestamp.display_string(), filename))
        lop_off = max(0, len(self.snapnames) - maxsnaps)
        self.snapnames = self.snapnames[lop_off:]
        self.handlesnaps(self.snapnames)


if __name__ == "__main__":
    def runwebcam():
        w = Webcam()
        while True:
            w.webcam_looponce()
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

