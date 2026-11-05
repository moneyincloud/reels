import sys, time, sherpa_onnx, soundfile as sf
M='/home/claude/models/sherpa-onnx-pocket-tts-int8-2026-01-26/'
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(pocket=sherpa_onnx.OfflineTtsPocketModelConfig(
 lm_flow=M+'lm_flow.int8.onnx',lm_main=M+'lm_main.int8.onnx',encoder=M+'encoder.onnx',decoder=M+'decoder.int8.onnx',
 text_conditioner=M+'text_conditioner.onnx',vocab_json=M+'vocab.json',token_scores_json=M+'token_scores.json'),num_threads=2,provider='cpu'))
tts=sherpa_onnx.OfflineTts(cfg)
ref,sr=sf.read(sys.argv[1],dtype='float32')
if ref.ndim>1: ref=ref[:,0]
g=sherpa_onnx.GenerationConfig(); g.reference_audio=ref; g.reference_sample_rate=sr; g.num_steps=int(sys.argv[4]) if len(sys.argv)>4 else 8
t=time.time(); a=tts.generate(open(sys.argv[2]).read().strip(),g)
sf.write(sys.argv[3],a.samples,a.sample_rate,subtype='PCM_16'); print(sys.argv[3],round(len(a.samples)/a.sample_rate,1),'s in',round(time.time()-t,1),'s')
