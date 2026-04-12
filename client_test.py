import requests
import textwrap

# Địa chỉ gốc của API đang chạy trên Colab
def test_url(base_url = "http://localhost:8000"):
    print("=========================================")
    print("1. KIỂM TRA ĐƯỜNG DẪN GỐC (GET /)")
    print("=========================================")
    try:
        response_root = requests.get(f"{base_url}/").json()
        print(response_root.get("message"))
        print("Tác giả:", response_root.get("author"))
        print("Mô hình:", response_root.get("model"))
        print("Dịch vụ:", response_root.get("usage"))
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}\n")

def test_health(base_url = "http://localhost:8000"):
    print("=========================================")
    print("2. KIỂM TRA TRẠNG THÁI SERVER (GET /health)")
    print("=========================================")
    try:
        response_health = requests.get(f"{base_url}/health")
        print(f"Mã trạng thái: {response_health.status_code}")
        print(f"Dữ liệu trả về: {response_health.json()}\n")
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}\n")

def test_api(base_url = "http://localhost:8000", message = ""):
    print("=========================================")
    print("3. KIỂM TRA TÓM TẮT VĂN BẢN (POST /generate)")
    print("=========================================")
    try:
        # Truyền tham số file_name="news_1" (đã tạo ở bước DATA PREPARATIONS)
        response_generate = requests.post(
                            f"{base_url}/generate", 
                            json={"message": message}, 
                            timeout=30)

        print(f"Mã trạng thái: {response_generate.status_code}")
        if response_generate.status_code == 200:
            result = response_generate.json().get("result")
            print("Kết quả tóm tắt:")
            wrapper = textwrap.TextWrapper(width=90, break_long_words=False, replace_whitespace=False)
            wrapped_result = wrapper.fill(result)

            print(f"-> {wrapped_result}\n")
        else:
            print(f"Lỗi từ server: {response_generate.text}")
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}\n")

