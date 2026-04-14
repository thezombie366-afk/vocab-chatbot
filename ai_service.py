import streamlit as st
import os
import json
import Lookup_service
import Quiz_service
import Fallout_hacking_game
get_word_details=Lookup_service.get_word_details
generate_guess_word=Quiz_service.genrate_guess_word
generate_quiz=Quiz_service.generate_quiz
Fallout_hacking_game=Fallout_hacking_game.fallout_hacking

#--------------------Lưu từ -------------------------------------
def save_word(data):
    # Đọc dữ liệu cũ từ file
    if os.path.exists("history.json") and os.path.getsize("history.json") > 0:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    # Kiểm tra trùng từ (theo 'word')
    existing_words = {item["word"] for item in history}
    if data["word"] not in existing_words:
        history.append(data)

        # Ghi lại toàn bộ vào file
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

        # Cập nhật session_state
        st.session_state.word_history = history
#-----------------------------------------------------------------------------------


