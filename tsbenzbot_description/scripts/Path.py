import speech_recognition as sr
from subprocess import call

s = '-s 140'
g = '-g 0.7'
f = '-vf3'
a = '-a 70'

list_room = ["mom bedroom","son bedroom","my bedroom","kitchen","living room"]



def Path_Create(y_top,y_bot,x_r,x_l):
    buffer = []
    count = 6
    diff = (x_l-x_r)/count
    for i in range(count):
        if (i%2 == 0):
            buffer.append([x_r+(i*diff),y_top,90])
            buffer.append([x_r+(i*diff),y_bot,0])
        else:
            buffer.append([x_r+(i*diff),y_bot,-90])
            buffer.append([x_r+(i*diff),y_top,0])         
    return buffer

if __name__ == '__main__':
    r = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_listen = r.listen(source, timeout=3.0)

        sound_cmd_in = r.recognize_google(audio_listen)
        sound_cmd_in = sound_cmd_in.lower()
        print(sound_cmd_in)
        for i in range(len(list_room)):  
            if list_room[i] in sound_cmd_in:
                call(['espeak', s, g, f, a, "OK, Cleaning" + list_room[i]])
                print(str(sound_cmd_in)+ "\n"+ str(list_room[i]))

    except sr.WaitTimeoutError:
        call(['espeak', s, g, f, a, "try again!"])
    except sr.UnknownValueError:
        call(['espeak', s, g, f, a, "try again!"])