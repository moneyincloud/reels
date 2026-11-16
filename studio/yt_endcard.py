"""Make the YouTube version of a reel: the reel + the 2.5 s SUBSCRIBE end card (studio/endcard/card.mp4).
usage: python3 studio/yt_endcard.py autopost/media/<name>.mp4      -> writes autopost/media/<name>-yt.mp4, prints its file name
Put that file name in the queue entry as  yt_video: <name>-yt.mp4  (Instagram keeps the original `video`)."""
import os, subprocess, sys
src = sys.argv[1]; out = src[:-4] + '-yt.mp4'
card = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'endcard', 'card.mp4')
fc = ('[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p,setsar=1[v0];'
      '[1:v]fps=30,format=yuv420p,setsar=1[v1];'
      '[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];'
      '[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-i', card, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
print(os.path.basename(out))
