from tkeasy import *
import webbrowser

title(text="Cards")

config(size="335x90+500+300",background="white")

frame1 = {"name_of_frame":"first_frame","background":"white","border_thickness":1,"border_color":"green","x":13,"y":5}
frame2 = {"name_of_frame":"second_frame","background":"white","x":10,"y":50}

filename = "words.txt"
i = 0

with open(filename) as f:
    content = f.readlines()

def next_word():
    global i
    i+=1
    try:
        label(frame=frame1,text=content[i].strip(),background="white",width=33,row=0,column=0)
    except:
        label(frame=frame1,text="End of file",background="white",width=35,row=0,column=0)  

def translate():
    url="https://translate.yandex.com/?lang=en-ru&text="+content[i].strip()
    webbrowser.open_new_tab(url)    

def images():
    url="https://yandex.ru/images/search?text="+content[i].strip()
    webbrowser.open_new_tab(url)   

def scrabble():
    url="https://www.thefreedictionary.com/words-that-start-with-"+content[i].strip()
    webbrowser.open_new_tab(url)  

button(frame=frame2,text="Следующее слово",command=next_word,row=1,column=1)
button(frame=frame2,text="Перевод",command=translate,row=1,column=2)
button(frame=frame2,text="Картинка",command=images,row=1,column=3)
button(frame=frame2,text="Разобрать",command=scrabble,row=1,column=4)

app_loop()