import speech_recognition as sr
import webbrowser
from datetime import datetime
import time
from gtts import gTTS
from playsound import playsound
import os
import random
import requests
from bs4 import BeautifulSoup

r = sr.Recognizer()

def record(ask = False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice = ""
        try:
            voice = r.recognize_google(audio, language='tr-tr')
        except sr.UnknownValueError:
            speak("Anlayamadim")
        except sr.RequestError:
            speak("Sistem calismiyor")
        return voice

def hava_durumu():
    url = "https://weather.com/az-AZ/weather/today/l/AJXX0001:1:AJ?Goto=Redirected"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    gelen_veri = soup.find_all("span", {"class": "CurrentConditions--tempValue--1RYJJ"})
    try:
        return gelen_veri[0].text
    except IndexError:
        return "Bulunamadi"

def response(voice):
    if "siri'yi tanıyor musun" in voice:
        speak("Siri benim baş düşmanlarımdan biri")
    if "nasilsin" in voice:
        speak("iyi senden")
    if 'saat kaç' in voice:
        speak(datetime.now().strftime('%H:%M:%S'))
    if 'arama yap' in voice:
        search = record('ne aramak istiyorsun')
        url = 'https://www.google.com/search?q='+search
        webbrowser.get().open(url)
        speak(search + ' için bulduklarım')
    if 'tamamdır' in voice:
        speak("Görüşürüz")
        exit()
    if "YouTube'da müzik ara" in voice or "YouTube'dan müzik ara" in voice or "YouTube'da bir şeyler ara" in voice :
        search1 = record('ne aramak istiyorsun')
        url1 = "https://www.youtube.com/results?search_query="+search1
        webbrowser.get().open(url1)
        speak(search1 + ' için bulduklarım')
    if "nasılsın" in voice or "Nasılsın" in voice:
        speak("teşekkürler Sen nasılsın")
    if "iyiyim" in voice:
        speak("iyi olmana sevindim")
    if "tanıyor musun" in voice:
        word = ["Pek tanıdık gelmedi",
                "Hayır tanımıyorum",
                "Belkide tanıyorumdur"]
        random_word = random.choice(word)
        speak(random_word)
    if "Sen bir robot musun" in voice:
        speak("Evet ben bir robotum ama akıllı ve planları olan bir robot")
    if "teşekkür ederim" in voice:
        speak("Ben teşekkür ederim")
    if "hava kaç derece" in voice or "hava" in voice:
        speak(f"Bugün Hava {hava_durumu()}")

def speak(string):
    tts = gTTS(string,lang='tr')
    rand = random.randint(1,10000)
    file = 'audio-'+str(rand)+'.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)

speak("nasıl yardımcı ola bilirim")
time.sleep(1)
while 1:
    voice = record()
    print(voice)
    response(voice)





















