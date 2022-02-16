import random
import pyttsx3
import datetime, time, os
import speech_recognition as sr
import wikipedia
import webbrowser
import keyboard
import pyowm
# import cv2 as cv
import requests
from bs4 import BeautifulSoup as bs
import serial
# import numpy, matplotlib, jupyterlab

#инициализация
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices)
owm = pyowm.OWM('8f649ebdb5b3cb03d3a4fb896ebb0c0e')

#списки
vihod = ["ещё увидимся","пока!","до свидания", "ухожу", "останавливаюсь"]
utro = ["доброе утро", "привет", "здравствуйте"]
vecher = ["добрый вечер", "здравствуйте", "привет", "добрый"]
den_ = ["добрый", "добрый день", "здравствуйте", "привет"]
noch = ["дорброй ночи", "время спатки", "здраствуйте"]
asist_names = ["ассистент", "Гена", "Азис", "генезис"] #"зис", "ген"
Headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50',
           'accept': '*/*}'} #
pechat = ["печатать", "напечатать", "пиши", "напиши", "писать", "написать", "печатай", "напечатай"]

def takeCommand():
    r = sr.Recognizer()
    r.pause_threshold = 0.5
    with open('resource.txt', 'a') as txt:
        with sr.Microphone() as mic_source:
            r.adjust_for_ambient_noise(source=mic_source, duration=0.5)
            print("Слушаю: ")
            audio = r.listen(mic_source)
            # audio = r.adjust_for_ambient_noise(source)
            try:
                print("распознавание...")
                query = r.recognize_google(audio, language='ru-RU')  # Используем google для распознания голоса.
                print(f"Вы сказали: {query}\n")  # Запрос пользователя выведен.
                txt.write(query + "\n")
            except Exception as e:
                # print(e)  используйте только если хотите видеть ошибку!
                print("Повторите ещё раз...")  # будет выведено, если речь не распознаётся
                return "Пусто"  # вернётся строка "Пусто"
            return query

def speak(audio):
    with open('resource.txt', 'a') as txt:
        engine.say(audio)
        engine.runAndWait()
        print(audio)
        txt.write(str(audio) + "\n")

def first_waking():
    tme = int(datetime.datetime.now().hour)
    now_time = str(tme)
    if tme >= 6 and tme <= 12:
        speak(random.choice(utro))
        speak(str(now_time))
    elif tme >= 13 and tme <= 17:
        speak(random.choice(den_))
        speak(str(now_time))
    elif tme >= 18 and tme <= 22:
        speak(random.choice(vecher))
        speak(str(now_time))
    elif tme >=23 or tme <= 5:
        speak(str(now_time))
        speak(random.choice(noch) + "кстати, пора спать")

def get_html_calc(url, params=None):
    r = requests.get(url, headers=Headers, params=params)
    return r
    pass

def get_content_calc(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('span', class_='qv3Wpe')
    ans = str(items)
    ans = ans.replace("span", "")
    time.sleep(0.2)
    ans = ans.replace("class", "")
    time.sleep(0.2)
    ans = ans.replace("qv3Wpe", "")
    time.sleep(0.2)
    ans = ans.replace("id", "")
    time.sleep(0.2)
    ans = ans.replace("cwos", "")
    time.sleep(0.2)
    ans = ans.replace("jsname", "")
    time.sleep(0.2)
    ans = ans.replace("VssY5c", "")
    time.sleep(0.2)
    ans = ans.replace("<", "")
    time.sleep(0.2)
    ans = ans.replace(">", "")
    time.sleep(0.2)
    ans = ans.replace("=", "")
    time.sleep(0.2)
    speak(ans)

def parse_calc(Url):
    html = get_html_calc(Url)
    if html.status_code == 200:
        get_content_calc(html.text)

def weather_parsing():
    while True:
        try:
            place = "Odessa"
            monitoring = owm.weather_manager().weather_at_place(place)
            weather = monitoring.weather
            # w = monitoring.get_weather()
            # temperature = w.get_temperature('celsius')
            status = weather.detailed_status
            temperatur = weather.temperature('celsius')
            temperature = temperatur['temp']
            # print(f'сейчас {status} в {place} . Температура - {temperature}')
            speak(f'сейчас {status} в {place} . Температура - {temperature} градусов по цельсию')
            break
        except:
            print("net.net")


def working(query, name_call):
    if 'википедия' in query:  # если wikipedia встречается в запросе, выполнится блок:
        speak("Поиск в Вики...")
        query = query.replace("википедия", "")
        query = query.replace("генезис", "")
        results = wikipedia.summary(query, sentences=7)
        speak("Запрос к Википедии")
        print(results)
        speak(results)
    elif "открыть телевизор" in query or "Открыть телевизор" in query:
        webbrowser.open("www.youtube.com")
        speak("открыт ютуб")
    elif "открыть Google" in query:
        webbrowser.open("google.com")
        speak("открыт гугл")
    elif "включи музыку" in query or "включить музыку" in query:
        music_dir = 'D:\Музыка'
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[random.randint(0, 120)]))
    elif "который час" in query or "время" in query or "сколько времени" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"время сейчас:  {strTime}")
    elif "тише" in query:
        keyboard.send('WIN+R')
        time.sleep(0.01)
        keyboard.write("cmd")
        time.sleep(0.5)
        keyboard.write('cd C:/Users/User/Desktop/')
        time.sleep(1)
        keyboard.send('enter')
        time.sleep(1)
        keyboard.write("setvol 10")
        time.sleep(0.5)
        keyboard.send('enter')
        time.sleep(4)
        keyboard.send('alt+F4')
        speak("звук на 10")
    elif "громче" in query:
        keyboard.send('WIN+R')
        time.sleep(0.01)
        keyboard.write("cmd")
        # os.startfile('C:/Windows/System32/cmd.exe')
        time.sleep(1)
        keyboard.write('cd C:/Users/User/Desktop/')
        keyboard.send('enter')
        time.sleep(1)
        keyboard.write("setvol 60")
        time.sleep(0.5)
        keyboard.send('enter')
        time.sleep(1.5)
        keyboard.send('alt+F4')
        speak("звук на 60")
    elif "молчать" in query:
        keyboard.send('FN+F7')
    elif "музыку на паузу" in query:
        keyboard.send('WIN+S')
        time.sleep(0.5)
        keyboard.write('му')
        time.sleep(0.5)
        keyboard.send('enter')
        time.sleep(1)
        keyboard.send('space')
        time.sleep(2)
        keyboard.send('ALT+TAB')
    elif "перезапусти программу" in query or "перезапустите программу" in query:
        keyboard.send('SHIFT+F10')
        keyboard.send('enter')
    elif "найти" in query:
        query = query.replace(name_call, "")
        query = query.replace("найти", "")
        webbrowser.open("https://www.google.com.ua/search?q=" + query)
    elif "посчитать" in query:
        # formula = query
        # formula = query.replace("посчитать", "")
        # formula = query.replace(name_call, "")
        query = query.replace(name_call, "")
        time.sleep(0.5)
        query = query.replace("посчитать", "")
        link = ("https://www.google.com.ua/search?q=" + query)
        webbrowser.open(link) #url="https://www.google.com.ua/search?q=" + formula
        parse_calc(link)
    elif "закрыть вкладку" in query or "закрой вкладку" in query:
        keyboard.send('Ctrl+F4')
    elif "переключить вкладку" in query or "переключи вкладку" in query:
        keyboard.send('Ctrl+Tab')
    elif "переключи окно" in query or "переключить окно" in query:
        keyboard.send('Alt+Tab')
    elif "какая температура"in query or "погода" in query:
        weather_parsing()
    elif "пластина" in query:
        query = query.replace(name_call, "")
        time.sleep(0.1)
        query = query.replace("пластина", "")
        output = int(query)
        print(query)
        for i in range(0, output):
            ser.write(1)
    elif "stop" in query or "стоп" in query or "остановись" in query:
        speak(random.choice(vihod))
        exit()
    for pechat_ in pechat:
        if pechat_ in query:
            query = query.replace(name_call, "")
            time.sleep(0.1)
            query = query.replace(pechat_, "")
            time.sleep(0.1)
            keyboard.write(query)

#еще инициализация:
#PySerial:
def error_arduino():
    speak("Ошибка инициализации Ардуино-пластины")
try:
    serialPort = 'COM5'
    baudRate = 9600
    ser = serial.Serial(serialPort, baudRate, timeout=0.5)
except: error_arduino()



if __name__=="__main__":
    try:first_waking()
    except: first_waking()
    while True:
        query = takeCommand().lower()
        # Приведём запрос к нижему регистру
        for element in asist_names:
            if element in query:
                print(element)
                working(query, element)
