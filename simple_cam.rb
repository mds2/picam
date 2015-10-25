require "date"

fork do
    `python -m SimpleHTTPServer`
end

seconds_between_shots = 60

numshots = 10
shots = 0.upto(numshots).map{|i| nil}
currshot = 0

while true do
  filename = "shots/#{DateTime.now.to_s}.jpg"
  shots[currshot] = filename
  `fswebcam -r 640x480 --set brightness=100% #{filename}`
  outfile = File::open("index.html", "w")
  outfile.write("<html><head><title>Stupid webcam tricks</title></head>\n")
  outfile.write("<body\n")
  0.upto(numshots).each do |idx|
    currfile = shots[(currshot + numshots - idx) % numshots]
    outfile.write("\n<img src=\"#{currfile}\"/><br/>\n")
  end
  outfile.write("<hr/><hr/><a href=\"shots/\">raw image files</a>")
  outfile.write("</body></html>")
  outfile.close()
  sleep seconds_between_shots
  currshot = (currshot + 1) % numshots
end
