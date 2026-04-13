Hệ Thống Tóm Tắt Văn Bản Tiếng Việt (Vietnamese Text Summarization API)

Mã sinh viên: 24120454

Họ và tên: Huỳnh Trần Phước Thiện

Học phần: Triển khai mô hình AI thực tế (Hugging Face to API)

Dự án này triển khai mô hình ngôn ngữ lớn Qwen2.5-1.5B-Instruct dưới dạng một dịch vụ API sử dụng FastAPI. Hệ thống cho phép người dùng gửi một đoạn văn bản dài và nhận lại bản tóm tắt súc tích, mạch lạc theo phong cách biên tập viên chuyên nghiệp.

Tính năng nổi bật
Mô hình AI: Sử dụng Qwen2.5-1.5B được tối ưu hóa (float16) để chạy mượt mà trên GPU T4 (Google Colab).

Kiến trúc: Tách biệt hoàn toàn giữa Logic AI (summarier.py), API Server (main.py) và Cấu hình (config.yaml).

Tiếng Việt chuyên sâu: System Prompt được tối ưu để tóm tắt tiếng Việt tự nhiên, không bị lai tạp ngôn ngữ.

Hỗ trợ từ xa: Tích hợp Ngrok để truy cập API công khai từ bất cứ đâu.

Cấu trúc dự án
main.py: Khởi tạo FastAPI server và các Endpoint.

summarier.py: Chứa class TextSummarizer xử lý nạp mô hình và thực hiện tóm tắt.

config.yaml: Quản lý đường dẫn mô hình và các tham số hệ thống.

client_test.py: Script Python hỗ trợ kiểm thử API tự động (Client-side).

requirements.txt: Danh sách các thư viện cần thiết.

requests.ipynb: Notebook hướng dẫn triển khai trên Google Colab.


Hướng dẫn cài đặt và triển khai
Bước 1: Chuẩn bị môi trường: Mở file requests.ipynb bằng Google Colab.
Đảm bảo đã chọn môi trường T4 GPU (Runtime > Change runtime type > T4 GPU).

Bước 2: Cài đặt thư viện
Chạy Cell đầu tiên trong Notebook hoặc sử dụng lệnh: pip install -r requirements.txt

Bước 3: Cấu hình Ngrok (Để lấy link truy cập công khai)
Đăng ký tài khoản miễn phí tại https://dashboard.ngrok.com/login.
Lấy Authtoken từ bảng điều khiển Ngrok.
Dán Token vào cell TẠO URL CHO DEMO cấu hình trong Notebook:

Bước 4: Khởi chạy Server
Chạy các cell tiếp theo để khởi động Server. Khi thấy dòng Application startup complete, một đường link có đuôi .ngrok-free.dev/.ngrok-free.app sẽ xuất hiện.

Hướng dẫn sử dụng
Cách 1: Sử dụng Swagger UI (Giao diện web)
Truy cập vào đường link Ngrok được cấp phát, thêm /docs vào cuối 
(Ví dụ: https://...ngrok-free.app/docs).
Tìm đến phương thức POST /generate.
Nhấn Try it out và nhập nội dung cần tóm tắt vào trường message.
Nhấn Execute để nhận kết quả.

Cách 2: Sử dụng Script Test (Giao diện Colab)
Sử dụng file client_test.py và các file new_1, new_2... đi kèm. Chỉ cần thay đổi base_url thành link Ngrok của mình và thay đổi file new mong muốn tóm tắt trong phần TEST API của request.ipynb. 

Link video demo: https://drive.google.com/drive/u/0/folders/1l475hd_n6uABdFgEZeH9_luLpzSyH3Kq
