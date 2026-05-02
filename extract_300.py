import zipfile
import os
import shutil

zip_path = r'C:\Users\NITRO\Downloads\archive.zip'
output_dir = r'C:\Users\NITRO\OneDrive\Desktop\CSDLDPT\audio'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

genres_to_extract = ['classical', 'jazz', 'reggae']
count = 0

print("Đang giải nén 300 file nguyên bản (30 giây/file) từ archive.zip...")

with zipfile.ZipFile(zip_path, 'r') as z:
    for filename in z.namelist():
        # Kiểm tra xem file có thuộc 3 thể loại trên và là file wav không
        if any(f'Data/genres_original/{genre}/' in filename for genre in genres_to_extract) and filename.endswith('.wav'):
            try:
                # Trích xuất tên file gốc (vd: classical.00000.wav)
                base_name = os.path.basename(filename)
                out_path = os.path.join(output_dir, base_name)
                
                # Copy file từ trong zip ra ngoài thư mục audio
                with z.open(filename) as source, open(out_path, "wb") as target:
                    shutil.copyfileobj(source, target)
                
                count += 1
            except Exception as e:
                pass

print(f"Hoàn thành! Đã copy {count} file nhạc nguyên bản (dài 30s) vào thư mục audio.")
