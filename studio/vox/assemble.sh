#!/bin/bash
# usage: assemble.sh <slug>   (run from studio/src)
set -e
S=$1
D=$(cd ../vox && python3 -c "import $S as M;print(round(M.DUR+0.5,3))")
printf "file '${S}_part0.mp4'\nfile '${S}_part1.mp4'\nfile '${S}_part2.mp4'\n" > ${S}_list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i ${S}_list.txt -c copy ${S}_vid.mp4
ffmpeg -y -loglevel error -loop 1 -t 0.5 -framerate 30 -i ../out/${S}_thumbnail.jpg -i ${S}_vid.mp4 -i ../$S/mix.wav -filter_complex "[0:v]scale=1080:1920,fps=30,format=yuv420p[c];[1:v]fps=30,format=yuv420p[m];[c][m]concat=n=2:v=1:a=0[v];[2:a]aresample=48000,adelay=500:all=1,apad[a]" -map "[v]" -map "[a]" -t $D -c:v libx264 -b:v 7000k -maxrate 7M -bufsize 14M -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ${S}_reel_raw.mp4
python3 ../vox/follow_overlay.py ${S}_reel_raw.mp4 ../out/${S}_final.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 ../out/${S}_final.mp4
