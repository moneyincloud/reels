import sys, subprocess, importlib
M=importlib.import_module(sys.argv[3]); render=M.render; DUR=M.DUR
FPS=30; N=int(DUR*FPS)
k,K=int(sys.argv[1]),int(sys.argv[2])
a=N*k//K; b=N*(k+1)//K
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-',
  '-c:v','libx264','-preset','medium','-crf','15','-pix_fmt','yuv420p',f'../src/{sys.argv[3]}_part{k}.mp4'],stdin=subprocess.PIPE)
for i in range(a,b): p.stdin.write(render(i/FPS).tobytes())
p.stdin.close(); p.wait(); print('done',k)
