from gtts import gTTS
import pygame
import time

# Urdu text
text = "آپ کی رپورٹ بالکل نارمل ہے، مبارک ہو!"

# Generate speech
tts = gTTS(text=text, lang='ur', slow=False)
tts.save("urdu_output.mp3")

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("urdu_output.mp3")
pygame.mixer.music.play()

# Wait till it's done playing
while pygame.mixer.music.get_busy():
    time.sleep(0.5)
