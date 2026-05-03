from gtts import gTTS
# Testing python test_audio.py

def text_to_speech_and_play(text, lang="en"):
    """Convert text to speech and play it through speakers"""
    try:
        tts = gTTS(text=text, lang=lang)
        output_file = "output.mp3"
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Test with a simple message
    text_to_speech_and_play("Hello, this is a test of the text to speech system.", "en")
