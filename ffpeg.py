# import subprocess as sp
# import sys

# from ffmpeg_progress import start


# def ffmpeg_callback(infile: str, outfile: str, vstats_path: str):
#     return sp.Popen(['ffmpeg',
#                      '-nostats',
#                      '-loglevel', '0',
#                      '-y',
#                      '-vstats_file', vstats_path,
#                      '-i', infile,
#                      '-crf','25',
#                      '-preset','veryfast',
#                      '-c:a','copy',
#                       outfile]).pid


# def on_message_handler(percent: float,
#                        fr_cnt: int,
#                        total_frames: int,
#                        elapsed: float):
#     sys.stdout.write('\r{:.2f}%'.format(percent))
#     sys.stdout.flush()


# start('https://coomer.party/d7/c7/d7c7aa652d69b552a0e58e5bc30d85e68832977c900e6f3279d7c6b44686b64f.m4v',
#       'testpy.mp4',
#       ffmpeg_callback,
#       on_message=on_message_handler,
#       on_done=lambda: print(''),
#       wait_time=0.5)  # seconds

from ffprobe import FFProbe

metadata=FFProbe('growinggirl1617_Thu, 10 Mar 2022 13:16:41 GMT.mp4')
print(metadata)
print(int(float(metadata.streams[0].duration)), metadata.streams[0].height, metadata.streams[0].width)

