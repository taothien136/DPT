import os
import random
import soundfile as sf
import shutil

src_dir = "audio_src"
out_dir = "audio"

# Backup original 30s files to audio_src if not already done
if not os.path.exists(src_dir):
    os.rename(out_dir, src_dir)
    os.makedirs(out_dir)
else:
    # Clear out_dir for fresh generation
    for f in os.listdir(out_dir):
        path = os.path.join(out_dir, f)
        if os.path.isfile(path):
            os.remove(path)

src_files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.endswith('.wav')]

def generate_crops(num_crops, duration_sec, prefix):
    for i in range(num_crops):
        src_file = random.choice(src_files)
        data, sr = sf.read(src_file)
        
        # calculate max start index
        samples_needed = int(duration_sec * sr)
        max_start = len(data) - samples_needed
        
        if max_start > 0:
            start_idx = random.randint(0, max_start)
        else:
            start_idx = 0
            
        cropped_data = data[start_idx:start_idx + samples_needed]
        
        out_name = f"{prefix}_{i+1:03d}_{os.path.basename(src_file)}"
        sf.write(os.path.join(out_dir, out_name), cropped_data, sr)

print("Đang cắt 300 bản nhạc độ dài 10 giây...")
generate_crops(300, 10, "track_10s")

print("Đang cắt 200 bản nhạc độ dài 15 giây...")
generate_crops(200, 15, "track_15s")

print("Hoàn thành tạo 500 file dữ liệu tổng hợp!")
