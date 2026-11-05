import sys, re, sherpa_onnx, soundfile as sf, numpy as np
exec(open('clone.py').read().split('ref,sr=')[0])
ref,sr=sf.read(sys.argv[1],dtype='float32')
g=sherpa_onnx.GenerationConfig(); g.reference_audio=ref; g.reference_sample_rate=sr; g.num_steps=10
lines=[l for l in re.split(r'(?<=[.!?])\s+',open(sys.argv[2]).read().strip()) if l]
out=[]
for l in lines:
    a=tts.generate(l,g); s=np.array(a.samples); out+= [s, np.zeros(int(a.sample_rate*0.25),np.float32)]
sf.write(sys.argv[3],np.concatenate(out),a.sample_rate,subtype='PCM_16'); print('ok')
