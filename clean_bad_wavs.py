import os
import soundfile as sf

audio_dir = "audio"
for f in os.listdir(audio_dir):
    if f.endswith('.wav'):
        path = os.path.join(audio_dir, f)
        try:
            sf.read(path)
        except Exception as e:
            print(f"Removing corrupted file: {f}")
            os.remove(path)
