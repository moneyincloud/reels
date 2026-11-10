import sys, sherpa_onnx, soundfile as sf
M='/home/claude/models/sherpa-onnx-whisper-small/'
lang=sys.argv[1]; task=sys.argv[2]
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'small-encoder.int8.onnx',decoder=M+'small-decoder.int8.onnx',tokens=M+'small-tokens.txt',language=lang,task=task,num_threads=4)
a,sr=sf.read(sys.argv[3],dtype='float32'); a=a if a.ndim==1 else a[:,0]
for i in range(0,len(a),sr*15):
    s=r.create_stream(); s.accept_waveform(sr,a[i:i+sr*15]); r.decode_stream(s); print(f'[{i//sr:>3}s]',s.result.text.strip(),flush=True)
