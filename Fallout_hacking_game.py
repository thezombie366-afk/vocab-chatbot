import random
def fallout_hacking(word_history):
    if len(word_history) == 0:
        print("ℹ️ Bạn cần tra cứu ít nhất một từ để có thể luyện tập!")
        print("Đang chọn một từ ngẫu nhiên từ lịch sử của bạn...")
        answer=random.choice(word_history['word'])
        quiz_data_3=answer
        return quiz_data_3