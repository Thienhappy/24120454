import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from omegaconf import OmegaConf

class TextSummarizer:
    def __init__(self, config_path):
        print("1. Đang đọc cấu hình...")
        self.config = OmegaConf.load(config_path)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"-> Đang sử dụng phần cứng: {self.device}")

        print("2. Đang tải Tokenizer thế hệ mới...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)

        print("3. Đang tải Siêu mô hình Qwen (Sẽ mất khoảng 1-2 phút)...")
        # Sử dụng torch.float16 để tiết kiệm RAM trên Colab
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        print("4. Đã khởi tạo thành công!")

    def __call__(self, message):
        messages = [
            {
                "role": "system",
                "content": (
                    "Bạn là một biên tập viên chuyên nghiệp. Hãy tóm tắt văn bản dưới đây thành một ĐOẠN VĂN DUY NHẤT "
                    "(khoảng 150-450 từ chỉ bao gồm tiếng Việt). Yêu cầu: Văn phong khách quan, các câu nối tiếp nhau mạch lạc bằng từ nối "
                    "(Ví dụ: 'Bên cạnh đó', 'Do đó', 'Chính vì vậy'). Tuyệt đối KHÔNG dùng gạch đầu dòng, "
                    "KHÔNG xưng 'Tôi' và KHÔNG thêm thông tin nằm ngoài bài viết."
                )
            },
            {"role": "user", "content": f"Hãy tóm tắt văn bản này:\n\n{message}"}
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                model_inputs.input_ids,
                max_new_tokens=700,     # Tăng lên 700 để đảm bảo không bị cụt chữ ở cuối
                min_new_tokens=200,     # Đặt tối thiểu 200 để tránh tóm tắt quá ngắn
                temperature=0.4,        # Giữ nhiệt độ thấp để AI tập trung, không lan man
                top_p=0.85,             # Giới hạn phạm vi từ vựng để tăng tính liên kết và tránh lạc đề
                do_sample=True,         # Kích hoạt chế độ sampling để tạo ra văn phong tự nhiên hơn, không quá máy móc 
                repetition_penalty=1.1  # Phạt nhẹ để tránh lặp từ nhưng vẫn giữ văn phong tự nhiên
            )

        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        summary = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        summary = summary.strip()
        return [{"summary_text": summary}]