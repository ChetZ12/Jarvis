import requests
import datetime
import random
import sys
import os
import smtplib
import webbrowser
import urllib
import pyttsx3
import speech_recognition as sr
import pyaudio
from PyDictionary import PyDictionary
from pygame import mixer

import ety
from nltk.corpus import wordnet

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-62)     # Slows down the speaking speed of the engine voice.

def speak(audio):
    print("  "+audio)
    engine.say(audio)
    engine.runAndWait()

def command():
    cmd = sr.Recognizer()
    with sr.Microphone() as source:
        cmd.adjust_for_ambient_noise(source)    # Adjusts the level to recieve voice even in case of noise in surroundings
        print('Listening..')
        audio = cmd.listen(source)
        try:
            query = cmd.recognize_google(audio,language='en-in')
            print('User: '+query+'\n')
        except sr.UnknownValueError:
            speak('Sorry ! I did not get that. Could you please type it out ?')
            query = str(input('Command: '))
    return query


def greeting():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12 :
        speak('Good Morning')
    if currentH >= 12 and currentH < 17 :
        speak('Good Afternoon')
    if currentH >= 17 and currentH != 0 :
        speak('Good Evening')
    
    
def find(name, path):
    for root, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def playOnYoutube(query_string):
    query_string = urllib.parse.urlencode({"search_query" : query})
    search_string = str("http://www.youtube.com/results?" + query_string)
    speak("Here's what you asked for. Enjoy!")
    webbrowser.open_new_tab(search_string)


def tellAJoke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept":"application/json"}
        )
    if res.status_code == 200:
        speak("Okay. Here's one")
        speak(str(res.json()['joke']))
    else:
        speak('Oops!I ran out of jokes')


greeting()
speak('jarvis here.')
speak('What would you like me to do for you ?')


if __name__ == '__main__':
    while True:

        query = command()
        query = query.lower()


        if 'play music' in query or 'play a song' in query :
             speak("Here's your music. Enjoy !")
             os.system('spotify')

        if 'find file' in query:
            speak('What is the name of the file that I should find ?')
            query = command()
            filename = query
            print(filename)
            speak('What would be the extension of the file ?')
            query = command()
            query = query.lower()
            extension = query
            print(extension)
            fullname = str(filename) + '.' + str(extension)
            print(fullname)
            path = r'D:\\'
            location = find(fullname,path)
            speak('File is found at the below location')
            print(location)

        if 'search' in query:
            speak('What should I search for ?')
            query = command()
            lib = query
            url = "https://www.google.co.in/search?q=" +(str(lib))+ "&oq="+(str(lib))+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
            webbrowser.open_new(url)

        if 'play on youtube' in query:
            speak('What should I look up for ?')
            query = command()
            playOnYoutube(query)            
       
        if 'joke' in query:
            tellAJoke()
        
        if 'open word' in query:
            os.system('libreoffice word')

        if 'send an email' in query:
            speak('whom would you like to send')
            query = command()
            sender = query
            speak('what would you like to send')
            query = command()

            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587) 

            # start TLS for security 
            s.starttls() 

            # Authentication 
            s.login("jarvisassistant.chetz@gmail.com", "jarvis@123") 

            # message to be sent 
            message = query

            # sending the mail 
            s.sendmail("jarvisassistant.chetz@gmail.com", sender, message) 

            # terminating the session 
            s.quit() 



        if 'that would be all' in query or 'that is it' in query or 'go to sleep jarvis' in query:
            speak('Alright. Have a nice day')
            sys.exit()
        if 'tell me about yourself' in query or 'who are you' in query:
            speak('i am jarvis, i was created by chethan and joljas. i am built to make your work simple and easier, i can do many task like sending an email or make u laugh and many more why dont you give a try on me?')
        if 'calculate for me' in query or 'open calculator' in query:
            os.system('gnome-calculator')
            