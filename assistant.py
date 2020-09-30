import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import random
from requests import get
import wolframalpha #For calculations
import pywhatkit as kit #To send whatsapp msgs

engine=pyttsx3.init('sapi5') 
voices=engine.getProperty('voices')

engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    speak("Whats your name")
    name=takeCommand().lower()
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning"+name)
    elif hour>=12 and hour<16:
        speak("Good Afternoon"+name)
    else:
        speak("Good Evening"+name)
    speak("I am your assistant today Please tell how may I help you?")

def takeCommand():
    #It takes microphone input from user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print ("Listening........")
        #seconds of non speaking audio before a phrase is considered complete
        r.pause_threshold = 1
       
        audio = r.listen(source)
    try:
        print ("Recognizing....")
        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        #print(e)
        print("Say that again please....")
        return "None"
    return query
def sendEmail(to,content):
    #Using SMTP protocol
    #Allow less secure apps in Gmail permissions
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com','your-password-here')
    server.sendmail('youremail@gmail.com',to,content)
    server.close()




if __name__ == "__main__":
    wishMe()
    while True:
        query=takeCommand().lower()
    #Logic for executing tasks based on query
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia......')
            query=query.replace("Wikipedia","")
            result=wikipedia.summary(query,sentences=2)
            speak("According to Wikipedia")
            print(result)
            speak(result)
        elif 'open notebook' in query:
            npath='C:\\Windows\\notepad.exe'
            os.startfile(npath)
        elif 'open adobe reader' in query:
            apath='C:\\Program Files (x86)\\Adobe\\Reader 9.0\\Reader\\AcroRd32.exe'
            os.startfile(apath)
        elif 'open command prompt' in query:
            os.startfile("start cmd")
        elif 'open camera' in query:
            capture=cv2.VideoCapture(0)
            while True:
                ret,img=capture.read()
                cv2.imshow('webcam',img)
                k=cv2.waitKey(50)
                if k==27:
                    break
            capture.release()
            cv2.destroyAllWindows()

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("Maam what should i search on google")
            cm=takeCommand().lower()
            webbrowser.open(f"{cm}")
        elif 'open facebook' in query:
            webbrowser.open("facebook.com")
        elif 'play music' in query:
            music_dir='E:\\Songs'
            songs=os.listdir(music_dir)
            #rd=random.choice(songs)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir,song))
        elif 'ip address' in query:
            ip = get('htps://api.ipify.org').text
            speak(f"Your ip address is {ip}")
        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Mam The time is {strTime}")
        elif 'open code' in query:
            codePath='C:\\Users\\ASUS\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code'
            os.startfile(codePath)
        #test code for sending email to one person if req more add dictionary
        elif 'email to anvita' in query:
            try:
                speak('What should I say')
                content=takeCommand()
                to= "recemail@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent")
            except Exception as e:
                print (e)
                speak("Sorry maam I couldn't send the email at the moment")

        elif 'send message' in query:
            speak("Maam what should i message")
            msg=takeCommand().lower()
            kit.sendwhatmsg("mobile-no",f"{msg}",23,21) #Enter the mobile no. and time in hours and minutes
        elif 'play songs on youtube' in query:
            speak("Maam what should i play on youtube")
            yt=takeCommand().lower()
            kit.playonyt(f"{yt}")
       
        elif "who are you" in query or "define yourself" in query: 
            para = '''Hello, I am Person. Your personal Assistant. 
            I am here to make your life easier. You can command me to perform 
            various tasks such as calculating sums or opening applications etcetra'''
            speak(para) 
        elif "who made you" in query or "created you" in query: 
            au = "I have been created by Anvita Gupta."
            speak(au)  
        elif "calculate" in query: 
            # write your wolframalpha app_id here 
            app_id = "WOLFRAMALPHA_APP_ID" 
            client = wolframalpha.Client(app_id) 
  
            indx = query.lower().split().index('calculate') 
            query1 = query.split()[indx + 1:] 
            res = client.query(' '.join(query)) 
            answer = next(res.results).text 
            speak("The answer is " + answer)   
         elif 'exit' in query or 'bye' in query:
            speak("Okay Bye")
            break





    
