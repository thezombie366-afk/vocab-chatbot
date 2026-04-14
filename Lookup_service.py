import streamlit as st
import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
load_dotenv(override=True) 
my_key = os.getenv("GOOGLE_API_KEY") 
genai.configure(api_key=my_key)
model = genai.GenerativeModel('gemini-2.5-flash')
#------------tra cứu--------------------------------------------------------
def get_word_details(word):
    """
    Gửi một yêu cầu đơn giản đến AI và in ra kết quả "thô".
    """
    print(f"\n--- Đang gửi yêu cầu cho từ: '{word}' ---")
    
    # Xây dựng chuỗi prompt (câu lệnh) đơn giản
    prompt = f"""
    Bạn là một dịch vụ API từ điển, chỉ trả về JSON.
    Hãy cung cấp thông tin cho từ: "{word}"
    
    Hãy trả lời CHỈ BẰNG một chuỗi JSON hợp lệ. 
    Đừng thêm bất kỳ văn bản giải thích nào, không dùng markdown (ví dụ: ```json).
    
    Nếu từ không tồn tại, hãy trả về một chuỗi JSON rỗng : {{
    }}

    Nếu từ tồn tại, hãy trả về một chuỗi JSON có cấu trúc :
    {{
      "definition": "định nghĩa bằng tiếng Việt", 
      "part_of_speech": "loại từ (ví dụ: danh từ, tính từ)", 
      "example": "một câu ví dụ bằng tiếng Anh"
    }}
    """
    
    try:
        # Gọi API để tạo nội dung
        response = model.generate_content(prompt)
        
        # 1. Lấy chuỗi JSON thô từ AI
        response_text = response.text

        # === BƯỚC QUAN TRỌNG: PARSE VÀ XỬ LÝ LỖI JSON ===
        try:
            data = json.loads(response_text)
            data['word'] = word.lower()
            return data

        except json.JSONDecodeError as e:
            # 4. Bắt lỗi NẾU AI trả về văn bản không phải JSON
            print(f"❌ LỖI PARSE JSON: AI đã không trả về JSON hợp lệ.")
            print(f"Lỗi chi tiết: {e}")
            print("Hãy thử kiểm tra lại prompt của bạn, hoặc AI đang gặp sự cố.")
    except Exception as e:
                print(f"Đã xảy ra lỗi hệ thống khi tra cứu: {e}")
                st.write({e})
#----------------------------------------------------------------------------------
