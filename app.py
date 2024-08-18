from flask import Flask, request, jsonify, render_template
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import pygame
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    target_lang = request.form['targetLang']
    r = sr.Recognizer()
    translated_text = ""
    while True:
        with sr.Microphone() as source:
            print("Listening... or say Exit to terminate")
            audio = r.listen(source)
            try:
                speech_text = r.recognize_google(audio)
                print(speech_text)
                if speech_text.lower() == "exit":
                    break
                translated_text = GoogleTranslator(source='auto', target=target_lang).translate(speech_text)
                print(translated_text)
                voice = gTTS(translated_text, lang=target_lang)
                voice.save("voice.mp3")
                pygame.mixer.init()
                # Use pygame.mixer for playing audio
                pygame.mixer.music.load("voice.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.quit()
                os.remove("voice.mp3")

            except sr.UnknownValueError:
                print("Cannot understand audio")
            except sr.RequestError:
                print("Could not request result")

            # Send the translated text back to the client-side
            if translated_text:
                return jsonify({
                    'translatedText': translated_text
                })

    # If "exit" is detected or an error occurs, return an empty response
    return jsonify({
        'translatedText': ""
    })

if __name__ == '__main__':
    app.run(debug=True)
