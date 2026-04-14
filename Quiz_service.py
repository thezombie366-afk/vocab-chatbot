import streamlit as st
import os
import google.generativeai as genai
import json
import random
from dotenv import load_dotenv
load_dotenv(override=True) 
my_key = os.getenv("GOOGLE_API_KEY") 
genai.configure(api_key=my_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#--------tạo câu đó 1--------------------------------------------------------------
def generate_quiz(word_history):
    """
    Chọn một từ ngẫu nhiên từ lịch sử để chuẩn bị tạo câu đố.
    """
    if len(word_history) == 0:
        print("ℹ️ Bạn cần tra cứu ít nhất một từ để có thể luyện tập!")
        return
    print("Đang chọn một từ ngẫu nhiên từ lịch sử của bạn...")
    random_item = random.choice(word_history)

    word = random_item.get('word')
    definition = random_item.get('definition')
    if not word:
         print("Lỗi: Không tìm thấy từ trong mục lịch sử. Hãy thử tra cứu lại.")
         return
    
    prompt = f"""
    Bạn là một chuyên gia tạo câu đố tiếng Anh (English Quiz Master).
    
    Nhiệm vụ: Hãy tạo một câu hỏi "điền vào chỗ trống" duy nhất sử dụng từ '{word}'.
    
    Bối cảnh: Từ được chọn là '{word}'. 
    (Gợi ý: Dùng định nghĩa '{definition}' làm bối cảnh cho câu hỏi nếu cần).

    Ràng buộc: Cung cấp 4 lựa chọn: 
    1. Một lựa chọn là đáp án đúng (chính là từ '{word}').
    2. Ba lựa chọn là các từ "mồi nhử" (distractors) hợp lý, có vẻ liên quan nhưng sai.

    Định dạng: Hãy trả lời CHỈ BẰNG một chuỗi JSON hợp lệ, không thêm bất kỳ văn bản nào khác.
    (như "Đây là câu đố của bạn:").
    Cấu trúc JSON bắt buộc:
    {{
      "question": "Câu hỏi với chỗ trống ____.", 
      "options": ["tùy chọn 1", "tùy chọn 2", "tùy chọn 3", "tùy chọn 4"], 
      "correct_answer": "{word}"
    }}
    """
    print("Đang gửi yêu cầu tạo câu đố đến AI...")
    try:
        # Chúng ta sử dụng lại biến 'model' đã khởi tạo ở đầu main.py
        response_raw = model.generate_content(prompt)
        response=response_raw.text.strip()
        if response.startswith("```"):
            response = response.strip("`")
    # loại bỏ nhãn 'json' nếu có
            response = response.replace("json\n", "").replace("json", "")
        quiz_data = json.loads(response)
        return quiz_data

    except json.JSONDecodeError as e:
        # Khối 'except' này đã có từ bài trước
        print(f"❌ LỖI PARSE JSON: AI đã không trả về JSON hợp lệ.")
        print(f"Lỗi chi tiết: {e}")
#-------------------------------------------------------------------------------------


#--------------------Tạo câu đó 2----------------------------------------------
def genrate_guess_word(word_history):
    if len(word_history) == 0:
        print("ℹ️ Bạn cần tra cứu ít nhất một từ để có thể luyện tập!")
        return
    print("Đang chọn một từ ngẫu nhiên từ lịch sử của bạn...")
    random_item = random.choice(word_history)

    quiz_data_2=random_item
    return quiz_data_2
#---------------------------------------------------------------------------------------