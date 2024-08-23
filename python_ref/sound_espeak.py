import os

def text_to_speech_espeak(text):
    os.system(f'espeak "{text}"')

if __name__ == "__main__":
    text = "Alexa... Good Morning"
    text_to_speech_espeak(text)
