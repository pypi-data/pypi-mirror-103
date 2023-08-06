'''this file would contain code that would fetch data and return it to user'''

import datetime
from .audioinout import speak
from datetime import date
def speaktime(format= 'thour'):
    if format == 'thour':
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")
    elif  format == 'tfhour':
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

def wishme(assistname = None):
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")
    if assistname is None:
        speak("I am your VirtualAssistant. Please tell me how may I help you")
    else:
        speak(f"I am {assistname}. Please tell me how may I help you")
        
def speakdate():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    speak(d2)
