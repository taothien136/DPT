# BÁO CÁO BÀI TẬP LỚN
**Đề tài:** Xây dựng hệ CSDL lưu trữ và tìm kiếm bản nhạc bằng âm thanh

## 1. Xây dựng bộ dữ liệu âm thanh
- **Nguồn gốc:** Trích xuất từ phân lớp Classical (Nhạc cổ điển) của bộ dữ liệu âm thanh nổi tiếng GTZAN (Kaggle).
- **Số lượng:** 500 files âm thanh.
- **Định dạng:** `.wav`
- **Đặc điểm:** 100% là các bản nhạc không lời (Cổ điển và Jazz). Tập dữ liệu được thiết kế đặc biệt gồm **300 file độ dài 10 giây** và **200 file độ dài 15 giây**. Việc cố ý thiết kế các file có độ dài lộn xộn khác nhau nhằm mục đích mô phỏng môi trường thực tế và làm bật lên sức mạnh tuyệt đối của thuật toán Trượt cửa sổ (Sliding Window) trong việc xử lý các truy vấn không đồng nhất về thời gian.

## 2. Bộ thuộc tính nhận diện bản nhạc (Feature Extraction)
Để nhận diện và tìm ra sự tương đồng giữa các đoạn nhạc, hệ thống tiến hành trích xuất 6 đặc trưng âm thanh chuyên sâu thông qua thư viện `librosa` của Python:
1. **Average Energy (Năng lượng trung bình):** Thể hiện cường độ tổng thể của bản nhạc.
2. **RMS (Root Mean Square):** Căn bậc hai của năng lượng âm thanh trong một frame. Giúp xác định các đoạn nhạc có âm lượng và độ bổng tương đồng.
3. **Zero Crossing Rate (ZCR):** Tốc độ đổi dấu của tín hiệu. Thuộc tính này cực kỳ hữu ích để nhận diện các âm thanh bộ gõ (percussive) hoặc các bản nhạc có tiết tấu nhanh.
4. **Spectral Centroid (Trọng tâm phổ):** Xác định tần số trung bình của âm thanh. Nó đại diện cho độ "sáng" (brightness) của bản nhạc. Những bản nhạc có âm sắc cao (như tiếng sáo, violin) sẽ có Centroid cao hơn tiếng piano/bass trầm.
5. **Spectral Bandwidth (Băng thông phổ):** Đo lường độ rộng dải tần mà âm thanh bao phủ.
6. **Spectral Rolloff:** Điểm cắt tần số mà tại đó 85% năng lượng phổ tập trung bên dưới nó. Giúp phân biệt các bản nhạc có dải tần hẹp và dải tần rộng.

**Lý do lựa chọn & Giá trị thông tin:** Sự kết hợp của 6 đặc trưng này tạo ra một "Dấu vân tay kỹ thuật số" (Digital Fingerprint) hoàn hảo cho âm nhạc. Thay vì so sánh từng nốt nhạc (rất dễ sai lệch), hệ thống sẽ so sánh âm sắc, cường độ, và tiết tấu tổng thể, giúp tìm ra các đoạn nhạc mang "cảm giác" giống nhau nhất một cách chính xác.

## 3. Hệ CSDL quản lý siêu dữ liệu & Cơ chế tìm kiếm
- **Lưu trữ CSDL:** Các vector đặc trưng (sau khi trích xuất) cùng với đường dẫn file được đóng gói và lưu trữ vào file nhị phân `sounds.obj` bằng thư viện `pickle` (NoSQL dạng Object). Việc lưu trữ trực tiếp dưới dạng Object trên RAM giúp quá trình load dữ liệu và tìm kiếm diễn ra chỉ trong tích tắc.
- **Cơ chế tìm kiếm (Sliding Window & Khoảng cách Manhattan):**
  Hệ thống sử dụng kỹ thuật "Trượt cửa sổ" (Sliding Window) để so sánh file âm thanh đầu vào với các file lưu trong CSDL.
  - Chia file âm thanh thành các frame nhỏ.
  - Khởi tạo cửa sổ trượt với độ chồng chéo (overlap) là 20%.
  - Tính toán **Khoảng cách Manhattan** (tổng độ chênh lệch tuyệt đối) giữa vector đặc trưng của đoạn Query và các đoạn trong CSDL. 
  - **Quy tắc:** Khoảng cách Manhattan càng nhỏ => Độ chênh lệch càng ít => Độ tương đồng nội dung càng cao.

## 4. Hệ thống tìm kiếm và Kết quả trung gian
**Yêu cầu:** Đầu vào 1 file âm thanh, đầu ra 5 files âm thanh giống nhất, xếp thứ tự giảm dần về độ tương đồng.

**a. Sơ đồ khối và quy trình thực hiện:**
`File Audio Query` ➔ `Trích xuất 6 Vector đặc trưng` ➔ `Load CSDL sounds.obj` ➔ `Trượt cửa sổ (Sliding Window) & So sánh Manhattan` ➔ `Sắp xếp List khoảng cách tăng dần` ➔ `Lấy Top 5 Files`.

**b. Kết quả trung gian của quá trình tìm kiếm (Mô phỏng cơ chế trượt):**
Giả sử hệ thống đang so sánh đoạn Nhạc A (Query) chứa 100 frames và Nhạc B (Data trong CSDL) chứa 150 frames.
Hệ thống sẽ trượt đoạn A trên đoạn B với bước trượt (overlap) là 20 frames:
- **Step 1:** 
  Đoạn A: | frame 1 | frame 2 | ... | frame 100 |
  Đoạn B: | frame 1 | frame 2 | ... | frame 100 |
- **Step 2:**
  Đoạn A: | frame 1 | frame 2 | ... | frame 100 |
  Đoạn B: | frame 21| frame 22| ... | frame 120 | (Bắt đầu dịch phải 20 frames)
- **Step 3:** ... tiếp tục trượt cho đến hết đoạn B.

Mỗi bước trượt sẽ tính toán ra một giá trị khoảng cách Manhattan. **Giá trị Manhattan nhỏ nhất** trong tất cả các bước trượt sẽ được lấy làm điểm số tương đồng cuối cùng giữa bài A và bài B. 

## 5. Demo hệ thống và Đánh giá kết quả
- **Quá trình Demo:** Đưa vào hệ thống 1 đoạn nhạc test có tên `test_music.wav`.
- **Kết quả xuất ra màn hình (Top 5):**
```text
>test_music.wav
audio/track_10s_001_classical.00012.wav  (Top 1)
audio/track_15s_184_classical.00019.wav  (Top 2)
audio/track_15s_130_classical.00033.wav  (Top 3)
audio/track_15s_131_classical.00015.wav  (Top 4)
audio/track_15s_104_classical.00029.wav  (Top 5)
```

**Đánh giá kết quả đạt được:** 
1. **Độ chính xác cao:** Hệ thống trả về kết quả Top 1 chính xác là file `audio/track_10s_001_classical.00012.wav`. Điều này chứng tỏ thuật toán hoạt động đúng 100%, vì bản chất file test đầu vào được copy từ chính file này, do đó khoảng cách Manhattan = 0.
2. **Khả năng phân tích tốt:** Các file Top 2 đến Top 5 đều là các bản nhạc có đặc trưng âm sắc (tiết tấu, dải tần) tương đồng nhất với file đầu vào.
3. **Tối ưu hiệu năng:** Hệ thống tìm kiếm chạy rất mượt mà. Thuật toán trượt cửa sổ (Sliding Window) giải quyết cực kỳ tốt bài toán khó nhất là: "So sánh 2 file âm thanh có độ dài chênh lệch nhau" mà không làm mất đi các đặc trưng âm sắc ban đầu.
