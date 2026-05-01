import zipfile
import os
import scipy.io.wavfile as wav
import io
import numpy as np

zip_path = r'C:\Users\NITRO\Downloads\archive.zip'
output_dir = r'C:\Users\NITRO\OneDrive\Desktop\CSDLDPT\audio'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

count = 0

print("Extracting and processing files...")

with zipfile.ZipFile(zip_path, 'r') as z:
    for filename in z.namelist():
        if 'Data/genres_original/classical/' in filename and filename.endswith('.wav'):
            # Read the audio file directly from the zip
            with z.open(filename) as f:
                try:
                    # scipy wavfile can read from a file-like object
                    # but we might need to read it into memory first
                    file_content = f.read()
                    sample_rate, data = wav.read(io.BytesIO(file_content))
                    
                    # File is 30 seconds long. We split into 5 parts of 6 seconds.
                    # Calculate number of samples per part
                    samples_per_part = len(data) // 5
                    
                    base_name = os.path.basename(filename).replace('.wav', '')
                    
                    for i in range(5):
                        start_idx = i * samples_per_part
                        end_idx = start_idx + samples_per_part if i < 4 else len(data)
                        
                        part_data = data[start_idx:end_idx]
                        
                        out_name = f"{base_name}_part{i+1}.wav"
                        out_path = os.path.join(output_dir, out_name)
                        
                        wav.write(out_path, sample_rate, part_data)
                        count += 1
                        
                except Exception as e:
                    print(f"Lỗi khi đọc file {filename}: {e}")

print(f"Successfully generated {count} files in audio folder!")
