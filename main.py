import requests , os , nest_asyncio , threading , uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

nest_asyncio.apply()

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

thread = threading.Thread(target=run_server, daemon=True)
thread.start()

from summarier import TextSummarizer
summarizer = TextSummarizer("config.yaml")


## TODO: Cập nhật Endpoint cho bài toán tóm tắt

@app.get("/")
async def root():
    return {
        "message": "Chào mừng đến với API Tóm tắt văn bản",
        "author": "Huỳnh Trần Phước Thiện - MSSV: 24120454",
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "usage": "Gửi dữ liệu POST tới /generate để tóm tắt văn bản."
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Server is running"}

@app.post('/generate')
async def generate_summary(message: str = Body(..., embed=True)):

    if not message or message.strip() == "":
        return {"message":message, "status":"error", "result": "Nội dung văn bản không được để trống."}

    try:
        summary = summarizer(message)
        return {"message":message,
                "status": "success", 
                "result": summary[0]['summary_text']}
    except Exception as e:
        return {"message":message, 
                "status": "error", 
                "result": f"Đã xảy ra lỗi: {str(e)}"}
    
## END TODO