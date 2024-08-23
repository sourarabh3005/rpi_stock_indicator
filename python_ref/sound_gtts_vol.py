from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def text_to_speech_gtts_with_volume(text, volume_change=0):
    # Generate the speech
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    
    # Load the audio file with pydub
    audio = AudioSegment.from_mp3("output.mp3")
    
    # Adjust the volume (in decibels)
    adjusted_audio = audio + volume_change  # Increase volume by n dB
    
    # Play the adjusted audio
    play(adjusted_audio)

if __name__ == "__main__":
    text = "Hello! This is a test of Google Text-to-Speech on Raspberry Pi."
    volume_change = 5  # Increase volume by 10 dB, decrease with negative values
    text_to_speech_gtts_with_volume(text, volume_change)
