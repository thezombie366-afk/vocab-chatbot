#----------Nhập-streamlit run app.py---------
import streamlit as st
import os
import json
import ai_service
import random
#----------------------------------------------- 
st.sidebar.title("Vocab Bot")
# Thêm một mô tả ngắn hoặc hướng dẫn vào sidebar
st.sidebar.info(
    "Đây là ứng dụng chatbot giúp bạn "
    "học và luyện tập từ vựng tiếng Anh bằng AI."
)
tab_lookup, tab_Practice = st.tabs(["Tra cứu", "Điền từ",])
# (Chúng ta cũng khởi tạo luôn cho quiz, sẽ dùng ở bài sau)




#-----------Khởi tạo history từ file history.json------------- dùng Ctrl+/

if "word_history" not in st.session_state:
    if os.path.exists("history.json") and os.path.getsize("history.json") > 0:
        with open("history.json", "r", encoding="utf-8") as f:
            st.session_state.word_history = json.load(f)
    else:
        st.session_state.word_history = []
#---------------------Test only----------------------------------

#----Sidebar history----------------------------------------------------------------
st.sidebar.subheader("Lịch sử tra cứu:")
seen_words = set()

for item in st.session_state.word_history:
    # kiểm tra trùng từ theo 'word'
    if item["word"] not in seen_words:
        seen_words.add(item["word"])
        with st.sidebar.expander(f"{item['word']} ({item['part_of_speech']})"):
            st.write("**Định nghĩa:**", item["definition"])
            st.write("**Ví dụ:**", item["example"])
#-------------------------------------------------------------------------------------

#---------------------------History expander------
with st.expander("Xem lịch sử tra cứu"):
    if not st.session_state.word_history:
        st.write("Lịch sử của bạn đang trống.")
    else:
        for item in st.session_state.word_history:
                with st.expander(f"{item['word']} ({item['part_of_speech']})"):
                    st.write("**Định nghĩa:**", item["definition"])
                    st.write("**Ví dụ:**", item["example"])
#-------------------------------------------



#--------------Kiểm tra trạng thái Quizz------
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""
#--------------------------------------------- 


#--------------Tra cứu--------------------------------------------------------------------    
with tab_lookup:
    st.header("Tra cứu từ vựng") 
    word_to_lookup = st.text_input("Enter your word:").lower()
    lookup_button = st.button("Look Up")
    if lookup_button:
        if word_to_lookup:
            with st.spinner(f"AI đang suy nghĩ về từ '{word_to_lookup}'..."):
                details = ai_service.get_word_details(word_to_lookup)
            if details.get('definition') != None:     
                st.success("Đã tìm thấy kết quả!")
                definition = details.get('definition', 'N/A')
                part_of_speech = details.get('part_of_speech', 'N/A')
                example = details.get('example', 'N/A')
                details['word'] = word_to_lookup
#--------------Lưu file từ vựng -------------------------- Dùng Ctrl+/
            if details.get('definition') != None:
                ai_service.save_word(details)
#----------------chỉ để test-------------------------------
                st.session_state.word_history.append(details)
                st.subheader(f"{word_to_lookup.capitalize()}") 
                st.write(f"**Định nghĩa:** {definition}")
                st.write(f"**Loại từ:** {part_of_speech}")
                st.write(f"**Ví dụ:** {example}")
            else:
             st.error("Sorry, I couldn't find that word or the AI failed to return valid JSON.")
                
                
        else:
            st.warning("Please enter a word.")
#--------------------------------------------------------------------------------------------------------

#---------------------------Quiz-----------------------------------------------------------------------------
with tab_Practice:
    st.header("Tạo bài luyện tập")
    makeQ_button = st.button('make quiz game')
    makeG_button = st.button('make guest game')


    if makeQ_button:
    
        # 1. Sử dụng lịch sử THẬT từ session state
        if not st.session_state.word_history:
            st.warning("Bạn cần tra cứu ít nhất một từ để luyện tập.")
        else:
            with st.spinner("AI đang tạo câu đố..."):
                # 2. Gọi AI service (đã làm ở bài trước)
                quiz_data = ai_service.generate_quiz(st.session_state.word_history)
            
            if quiz_data:
                # 3. LƯU câu đố vào "bộ nhớ"
                st.success('tạo quiz thành công')
                st.session_state.current_quiz = quiz_data
                # Xóa (hoặc comment out) dòng st.json(quiz_data) cũ
            else:
                st.error("Lỗi: Không thể tạo câu đố từ AI.")   
    if st.session_state.current_quiz:

        quiz = st.session_state.current_quiz
        st.write(quiz.get('question', 'Lỗi: Không tìm thấy câu hỏi.'))
        if "last_quiz_id" not in st.session_state or st.session_state.last_quiz_id != id(quiz):
            options_list = quiz.get('options', [])
            random.shuffle(options_list)
            st.session_state.shuffled_options = options_list
            st.session_state.last_quiz_id = id(quiz)
        options_list = st.session_state.shuffled_options
        user_choice = st.radio(
            "Chọn đáp án đúng:",
            options_list,
            index=None,
            key=f"quiz_{st.session_state.last_quiz_id}"
        )
        if user_choice is not None:
            if user_choice == quiz['correct_answer']:
                st.success(f"Đúng rồi! Đáp án là '{user_choice}'")
                st.balloons()
                st.session_state.current_quiz = None
            else:
                st.error(f"Sai rồi... Hãy thử lại!")
            
    
    if makeG_button:
        if not st.session_state.word_history:
            st.warning("Bạn cần tra cứu ít nhất một từ để luyện tập.")
        else:
            with st.spinner("AI đang tạo câu đố..."):
                st.session_state.quiz_data = ai_service.generate_guess_word(st.session_state.word_history)
            st.session_state.user_answer = ""
    if st.session_state.quiz_data:
        st.write("Hãy điền từ theo định nghĩa sau:")
        st.write(st.session_state.quiz_data.get("definition"))

        st.session_state.user_answer = st.text_input(
            "Câu trả lời của bạn:",
            value=st.session_state.user_answer,
            key="quiz_input"
        )
        if st.button("Kiểm tra Đáp án"):
            if not st.session_state.user_answer.strip():
                st.warning("Bạn chưa nhập đáp án nào!")
            elif st.session_state.user_answer.strip().lower() == st.session_state.quiz_data.get("word").lower():
                st.success(f"Đúng rồi! Đáp án là '{st.session_state.quiz_data.get('word')}'")
                st.balloons()
                st.session_state.current_quiz = None
            else:
                st.error("Sai rồi... Hãy thử lại!")
#-------------------------------------------------------------------------------------------------------------------


#---------------------------Fallou4_hacking-----------------------------------------------------------------------------
# with tab_Practice_2:
#     st.header("Fallout4_hacking")
#     makeH_button = st.button("Luyện tập Fallout4_h")
#     if makeH_button:
#         for ques in st.session_state.word_history['word']:
#             st.button(ques)
            
#-------------------------------------------------------------------------