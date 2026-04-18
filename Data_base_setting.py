import sqlite3

# Hàm khởi tạo DB và tạo bảng nếu chưa có
def init_db():
    conn = sqlite3.connect("vocab.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            definition TEXT,
            part_of_speech TEXT,
            example TEXT
        )
    """)
    conn.commit()
    conn.close()
def get_all_words():
    conn = sqlite3.connect("vocab.db")
    cursor = conn.cursor()
    cursor.execute("SELECT word, definition, part_of_speech, example FROM vocab")
    rows = cursor.fetchall()
    conn.close()
    # Chuyển thành list[dict]
    return [
        {"word": r[0], "definition": r[1], "part_of_speech": r[2], "example": r[3]}
        for r in rows
    ]
def save_word(details):
    conn = sqlite3.connect("vocab.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO vocab (word, definition, part_of_speech, example)
        VALUES (?, ?, ?, ?)
    """, (
        details["word"],
        details.get("definition", ""),
        details.get("part_of_speech", ""),
        details.get("example", "")
    ))
    conn.commit()
    conn.close()
init_db()