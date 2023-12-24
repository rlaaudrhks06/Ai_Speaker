import speech_recognition as sr
from gtts import gTTS
import playsound
import requests
import json
import os
import osascript
import re
import webbrowser

## 날씨 api
city = "Seoul"
apikey = "349a85551aec75a623d926c4aaf47aa9"
lang = "kr"
api = f"""http://api.openweathermap.org/data/2.5/\
weather?q={city}&appid={apikey}&lang={lang}&units=metric"""
result = requests.get(api)
data = json.loads(result.text)

## TTS
def speak(text, speed=False):
     tts = gTTS(text=text, lang='ko', slow=speed)
     filename=text+'.mp3'
     tts.save(filename)
     playsound.playsound(filename)

## STT
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("무엇을 도와드릴까요?")
        print("Listening : ")
        audio = r.listen(source)
    print(r.recognize_google(audio, language='ko-KR'))
    voice = [r.recognize_google(audio, language='ko-KR')]
    ## Funtion
    for i in voice:
        if '안녕' in i:
            speak("반가워요.")
        elif '종료' in i:  
            speak("종료할게요.")
            break
        elif '구글' in i or '크롬' in i:
            url = 'Chrome://new-tab-page'
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
            webbrowser.get(chrome_path).open(url)
            speak('구글 새창을 열었어요.')

        elif '볼륨' in i or '소리' in i :
            numbers = re.findall(r'\d+', i)
            vol = "set volume output volume " + numbers[0]
            print(str(numbers))
            osascript.osascript(vol)
            speak('소리를' + numbers[0] + '으로 바꿨어요.')
            
        elif '날씨' in i:
            if data["main"]["feels_like"] <= 4:
                speak("체감온도는"+str(data["main"]["feels_like"])+"도이고 패딩과 두꺼운 코트를 추천합니다.")
            elif data["main"]["feels_like"] >= 5 and data["main"]["feels_like"] <= 8:
                speak("체감온도는"+str(data["main"]["feels_like"])+"도이고 울코트와 가죽 옷을 추천합니다.")
            elif data["main"]["feels_like"] >= 9 and data["main"]["feels_like"] <= 16:
                speak("체감온도는"+str(data["main"]["feels_like"])+"도이고 점퍼과 기모바지를 추천합니다.")
            elif data["main"]["feels_like"] >= 17 and data["main"]["feels_like"] <= 19:
                speak("체감온도는"+str(data["main"]["feels_like"])+"도이고 니트와 가디건을 추천합니다.")
            elif data["main"]["feels_like"] >= 20 and data["main"]["feels_like"] <= 22:
                speak("체감온도는"+str(data["main"]["feels_like"])+"도이고 긴팔티와 면바지를 추천합니다.")
            elif data["main"]["feels_like"] >= 23 and data["main"]["feels_like"] <= 27:
                speak("체감온도는"+str(data["main"]["feels_like"])+"도이고 반팔과 반바지를 추천합니다.")
            else:
                speak("체감온도는"+str(data["main"]["feels_like"])+"도이고 민소매와 반바지를 추천합니다.")
        else:
            speak("잘 못알아들었어요.")
    break
