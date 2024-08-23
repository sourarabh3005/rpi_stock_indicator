from gtts import gTTS
import os

def text_to_speech_gtts(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Use mpg321 to play the audio file

if __name__ == "__main__":
    #text = "Hello! This is a test of Google Text-to-Speech on Raspberry Pi."
    text = "Alexa... Play songs by K K"
    text_to_speech_gtts(text)
