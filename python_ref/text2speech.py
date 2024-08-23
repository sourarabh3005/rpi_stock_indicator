import pyttsx3

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # You can set properties like voice, rate, and volume if needed
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Convert the text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

if __name__ == "__main__":
    # Example text input
    text = "Hello! This is a text-to-speech test on Raspberry Pi."
    
    # Call the function to convert text to speech
    text_to_speech(text)