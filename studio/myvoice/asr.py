import sys, sherpa_onnx, soundfile as sf, numpy as np
M='/home/claude/models/sherpa-onnx-whisper-base.en/'
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'base.en-encoder.int8.onnx',decoder=M+'base.en-decoder.int8.onnx',tokens=M+'base.en-tokens.txt',num_threads=2)
for f in sys.argv[1:]:
    a,sr=sf.read(f,dtype='float32'); a=a if a.ndim==1 else a[:,0]
    out=[]
    for i in range(0,len(a),sr*28):
        s=r.create_stream(); s.accept_waveform(sr,a[i:i+sr*28]); r.decode_stream(s); out.append(s.result.text.strip())
    print(f,':',' '.join(out))
