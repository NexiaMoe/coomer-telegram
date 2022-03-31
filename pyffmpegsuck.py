import base64



in_file = open("ffmpeg-release-amd64-static.tar.xz.0", "rb") # opening for [r]eading as [b]inary
data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
in_file.close()

data = base64.b64encode(data)

out_file = open("linux.py", "w") # open for [w]riting as [b]inary
out_file.write(f"contents={data}")
out_file.close()