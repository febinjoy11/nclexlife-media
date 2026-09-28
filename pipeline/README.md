# NCLEX.life Shorts pipeline

Renders a ~23 s 1080x1920 animated quiz Short from one JSON config.

Setup (each run):
```
pip install numpy pillow soundfile kokoro-onnx
curl -L -o kokoro16.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.fp16.onnx
curl -L -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
export KOKORO_MODEL=kokoro16.onnx KOKORO_VOICES=voices.bin
```
Render:
```
python engine.py prep   config.json work     # warns OVER if a voice line is too long: shorten it and rerun
python engine.py render config.json work 0 400
python engine.py render config.json work 400 800
python engine.py final  config.json work short.mp4
python engine.py still  config.json work 1 10.5 14 18   # preview frames for QA
```
Scenes: `airborne`, `priority`, `sort` (two-column sorting, e.g. RN/UAP or GIVE/HOLD), fallback `flow`.
Timeline: hook 0-1.4 s, question, options 3.5 s, PICK ONE 5.9 s, countdown 6.4-9.4 s, reveal 9.4 s, explanation 11.8 s, memory rule 16.8 s, engage/next 19.8-23.3 s.

content_log.csv = every video made so far. Check it before choosing a topic; append after scheduling.
