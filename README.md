# 🤖 DiscQuizBOT

**DiscQuizBOT** là một bot Discord hỗ trợ tạo câu hỏi từ các tài liệu như PDF, Word bằng AI. Bot sử dụng **Gemini AI** và có thể đọc, tóm tắt nội dung, sau đó tạo câu hỏi để giúp người dùng ôn tập dễ dàng hơn. 📚✨

---

## 🔥 Cài Đặt và Khởi Chạy Bot

### 1️⃣ Tạo môi trường ảo (Virtual Environment)
Mở terminal/cmd trong thư mục của dự án và chạy lệnh sau:
```sh
python -m venv .venv
```

### 2️⃣ Kích hoạt môi trường ảo
#### 🔹 Windows:
```sh
.venv\Scripts\activate
```
#### 🔹 macOS/Linux:
```sh
source .venv/bin/activate
```

### 3️⃣ Cài đặt các thư viện cần thiết
Chạy lệnh sau để cài đặt các dependencies:
```sh
pip install discord.py python-docx PyPDF2 requests google.generativeai
```

---

## 🛠 Cấu Hình API Key

### 🔹 Cấu hình API Key cho Gemini AI và Discord Bot
Để bot hoạt động, bạn cần tạo và cung cấp API Key:
1. **Discord Bot Token**: Lấy từ [Discord Developer Portal](https://discord.com/developers/applications).
2. **Gemini AI API Key**: Lấy từ Google AI.

Thêm chúng vào file `.env` hoặc trực tiếp trong mã nguồn nếu cần.

---

## 📁 Các File Quan Trọng

| 📌 File | 📝 Mô tả |
|---------|---------|
| `DiscQuizBOT.py` | File chính chứa mã nguồn của bot. |
| `README.md` | Hướng dẫn cài đặt và sử dụng bot. |
| `requirements.txt` | Danh sách các thư viện cần thiết. |

---

## 🚀 Khởi Chạy Bot
Sau khi cài đặt và cấu hình API Key, bạn có thể chạy bot bằng lệnh:
```sh
python DiscQuizBOT.py
```
Nếu bot khởi chạy thành công, nó sẽ xuất hiện trong server Discord của bạn! 🎉

---

## 📌 Ghi Chú
- Nếu gặp lỗi, hãy kiểm tra lại API Key hoặc cài đặt thư viện.
- Đọc tài liệu chính thức của `discord.py` nếu cần hỗ trợ nâng cao.

🌟 **Chúc bạn học tập hiệu quả với DiscQuizBOT!** 🚀

