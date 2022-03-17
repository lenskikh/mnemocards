from tkeasy import *
import webbrowser
import random
import subprocess
import os

title(text="Cards")

config(size="445x155+700+300",background="white")

frame1 = {"name_of_frame":"first_frame","background":"white","border_thickness":1,"border_color":"green","x":13,"y":13}
buttons = {"name_of_frame":"second_frame","background":"white","x":13,"y":83}
icons = {"name_of_frame":"icons","background":"white","x":400,"y":20}

tabs = {"File":{"New":"False","Open":"False","Save":"False","Save as":"False","Close":"False","---":"---","Exit":quit},
"Edit":{"Undo":"False","---":"---","Cut":"False","Copy":"False","Paste":"False","Delete":"False","Select All":"False"},
"Help":{"Help Index":"False","About...":"False","Help":"False"}}

top_menu(tabs)

filename = "eng_rus.csv"
i = 0
win = ""

with open(filename, encoding="UTF-8") as f:
    content = f.readlines()

def first_column():
    return content[i].strip().split(";")[0]

#separates a word from a transcription
def find_word():
    word = content[i].strip().split(";")[0]
    return word.strip().split("[")[0]

def second_column():
    return content[i].strip().split(";")[1]

def third_column():
    return content[i].strip().split(";")[2]    

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
    photo_click().bind("<Button-1>",lambda url:second_window("original",""))

    photo(frame=icons,file="icons/edit.png",row=1,column=0)
    photo_click().bind("<Button-1>",lambda url:second_window("translate",""))    

def check_in_web():
    url="https://translate.yandex.com/?lang=en-ru&text="+find_word()
    webbrowser.open_new_tab(url)   

def translate():
    word = second_column()
    make_label(word,1,0) 

def mnemocard():
    second_window("mnemo","mnemo_label")

def rules():
    win=str(random.random())
    window_2 = {"name_of_frame":str(random.random()),"padx":5,"pady":5}
    config(window=win,frame=window_2,size="400x320+600+300",background="white")
    title(window=win,frame=window_2,text="Правила построения")
    label(window=win,frame=window_2,text="Test",background="white",width=42,row=0,column=0)

def new_word():
    win=str(random.random())
    window_2 = {"name_of_frame":str(random.random()),"background":"white","padx":5,"pady":5}
    config(window=win,frame=window_2,size="345x320+600+300",background="white")  
    title(window=win,frame=window_2,text="Новое слово") 
    #original
    label(window=win,frame=window_2,text="Оригинальное слово",background="white",row=0,column=0)
    entry(window=win,frame=window_2,name="entry 1",inner_border=4,background="lightyellow",justify="center",row=1,column=0) 

    #translate
    label(window=win,frame=window_2,text="Перевод",background="white",row=2,column=0)
    text_area(window=win,frame=window_2,name="area",background="lightyellow",inner_border=4,width=40,height=3,row=3,column=0)
    
    #mnemo phase
    label(window=win,frame=window_2,text="Мнемо-фраза",background="white",row=4,column=0)
    text_area(window=win,frame=window_2,name="mnemoarea",background="lightyellow",inner_border=4,width=40,height=4,row=5,column=0)

    def save_new_word():
        content = get_info("entry 1")+";"+get_info("area").strip()+";"+get_info("mnemoarea").strip()+";"+"\n"

        with open(filename, 'a+', encoding="UTF-8") as file:
            file.write(content)        

    button(window=win,frame=window_2,text="Сохранить",command=save_new_word,row=6,column=0)

def second_window(what_type, special):
    global win #for close window
    win=str(random.random())
    window_2 = {"name_of_frame":str(random.random()),"padx":5,"pady":5}
    config(window=win,frame=window_2,size="400x320+600+300",background="white")
    title(window=win,text="Add translate")

    text_area(window=win,frame=window_2,name="entry2",height=15,width=48,row=0,column=0)  

    if what_type == "translate":
        insert_text_area(name="entry2",text=second_column(),color = "black")
        button(window=win,frame=window_2,text="Сохранить",command=add_translate,row=2,column=0)
    elif what_type == "original":
        insert_text_area(name="entry2",text=first_column(),color = "black")
        button(window=win,frame=window_2,text="Сохранить",command=add_original,row=2,column=0)
    elif what_type == "mnemo":
        insert_text_area(name="entry2",text=third_column(),color = "black")

    if special == "mnemo_label":
        button(window=win,frame=window_2,text="Правила мнемоники",command=rules,row=1,column=0)
        button(window=win,frame=window_2,text="Сохранить",command=add_mnemo,row=2,column=0)
    else:
        button(window=win,frame=window_2,text="Проверить в Yandex",command=check_in_web,row=1,column=0)

def add_original():
    word2 = get_info("entry2")
    content[i] = word2.strip()+";"+second_column()+"\n"
    save_to_file(content)

def add_translate():
    word2 = get_info("entry2")
    content[i] = first_column()+";"+word2.strip()+";"+"\n"
    save_to_file(content)

def add_mnemo():
    word2 = get_info("entry2")
    content[i] = first_column()+";"+second_column()+";"+word2.strip()+";"+"\n"
    save_to_file(content)

def delete_card():
    content[i] = ""
    save_to_file(content)    

def save_to_file(content):
    with open(filename, 'w', encoding="UTF-8") as file:
        for n in content:
            file.write(n)
    msg_box_warning("warning","Сохранено!")
    quit(window=win)    

def images():
    url="https://yandex.ru/images/search?text="+find_word()
    webbrowser.open_new_tab(url)   

def scrabble():
    url="https://www.thefreedictionary.com/words-that-start-with-"+find_word()
    webbrowser.open_new_tab(url)  

#Empty screen on the start
make_label("",0,0)
make_label("",1,0)

#Buttons
button(frame=buttons,text="Предыдущее слово",command=counter_minus,row=1,column=0)
button(frame=buttons,text="Следующее слово",command=counter_plus,row=1,column=1)
button(frame=buttons,text="Мнемо",command=mnemocard,row=1,column=2)
button(frame=buttons,text="Перевод",command=translate,row=1,column=3)

button(frame=buttons,text="Добавить карту",command=new_word,row=2,column=0)
button(frame=buttons,text="Удалить карту",command=delete_card,row=2,column=1)
button(frame=buttons,text="Перешать карты",command=False,row=2,column=3)
button(frame=buttons,text="Варианты",command=scrabble,row=2,column=2)

app_loop()