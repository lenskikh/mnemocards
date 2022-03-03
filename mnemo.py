from tkeasy import *
import webbrowser
import random

title(text="Cards")

config(size="450x110+700+300",background="white")

frame1 = {"name_of_frame":"first_frame","background":"white","border_thickness":1,"border_color":"green","x":13,"y":5}
frame2 = {"name_of_frame":"second_frame","background":"white","x":10,"y":70}
icons = {"name_of_frame":"icons","background":"white","x":400,"y":10}
frame_for_second_window = {"name_of_frame":str(random.random()),"padx":5,"pady":5}

filename = "eng_rus.csv"
i = 0
win = ""

with open(filename, encoding="UTF-8") as f:
    content = f.readlines()


def first_column():
    return content[i].strip().split(";")[0]

def second_column():
    return content[i].strip().split(";")[1]

def make_label(word,row,column):
    return label(frame=frame1,text=word,background="white",width=45,row=row,column=column)

def counter_minus():
    global i
    i-=1
    next_word()

def counter_plus():
    global i
    i+=1
    next_word()

def next_word():
    try:
        word = first_column()
        make_label(word,0,0) 
    except:
        #End of file
        make_label("End of file",0,0) 

    #clear line for the next word
    make_label("",1,0)  

    #Edit
    photo(frame=icons,file="icons/edit.png",row=0,column=0)
    photo_click().bind("<Button-1>",lambda url:second_window())

def check_in_web():
    url="https://translate.yandex.com/?lang=en-ru&text="+first_column()
    webbrowser.open_new_tab(url)   

def translate():
    word = second_column()
    make_label(word,1,0) 
    photo(frame=icons,file="icons/edit.png",row=1,column=0)
    photo_click().bind("<Button-1>",lambda url:second_window())

def second_window():
    global win #for close window
    win=str(random.random())

    config(window=win,frame=frame_for_second_window,size="400x320+600+300",background="white")
    title(window=win,text="Add translate")
    text_area(window=win,frame=frame_for_second_window,name="entry2",height=15,width=48,row=0,column=0)
    insert_text_area(name="entry2",text=second_column(),color = "black")
    button(window=win,frame=frame_for_second_window,text="Проверить в Yandex",command=check_in_web,row=1,column=0)
    button(window=win,frame=frame_for_second_window,text="Добавить",command=add_translate,row=2,column=0)

def add_translate():
    word2 = get_info("entry2")
    content[i] = first_column()+";"+word2.strip()+";"+"\n"

    with open(filename, 'w', encoding="UTF-8") as file:
        for n in content:
            file.write(n)
    msg_box_warning("warning","Добавлено!")
    quit(window=win)

def images():
    url="https://yandex.ru/images/search?text="+first_column()
    webbrowser.open_new_tab(url)   

def scrabble():
    url="https://www.thefreedictionary.com/words-that-start-with-"+first_column()
    webbrowser.open_new_tab(url)  

#Empty screen on the start
make_label("",0,0)
make_label("",1,0)

#Buttons
button(frame=frame2,text="Предыдущее слово",command=counter_minus,row=1,column=1)
button(frame=frame2,text="Следующее слово",command=counter_plus,row=1,column=2)
button(frame=frame2,text="Перевод",command=translate,row=1,column=3)
button(frame=frame2,text="Мнемо",command=images,row=1,column=4)
button(frame=frame2,text="Варианты",command=scrabble,row=1,column=5)

app_loop()