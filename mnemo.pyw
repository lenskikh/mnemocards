from tkeasy import *
import webbrowser
import random
import json
import os

title(text="Cards")

config(size="480x160+700+300",background="white")

frame1 = {"name_of_frame":"first_frame","background":"white","border_thickness":1,"border_color":"green","x":13,"y":13}
buttons = {"name_of_frame":"second_frame","background":"white","x":9,"y":83}
icons = {"name_of_frame":"icons","background":"white","x":440,"y":20}

i = 0 #counter for words
win = ""

def english():
    save_settings("eng")
    global interface
    interface = load_lang("english.json")

def russian():
    save_settings("rus")
    global interface
    interface = load_lang("russian.json")    

def load_lang(filename):
    with open(filename, encoding="UTF-8") as f:
        content = f.read()

    interface = json.loads(content)
    return interface

def start_settings():
    with open("lang_settings.txt", encoding="UTF-8") as f:
        for i in f:
            if "eng" == i:
                english()
            elif "rus" == i:
                russian()

def load_direction():
    with open("direction.txt", encoding="UTF-8") as f:
        for i in f:
            return i

filename = load_direction()
with open(filename, encoding="UTF-8") as f:
    content = f.readlines()

def switch_to(switch):
    if switch == "russian":
        russian()
        #restart_app()
        msg_box_warning("warning",interface["restart"])
    elif switch == "english":
        english()
        #restart_app()
        msg_box_warning("warning",interface["restart"])

def column_original_word():
    return content[i].strip().split(";")[0]

#separates a word from a transcription
def column_transcription():
    return content[i].strip().split(";")[1]

def column_translate():
    return content[i].strip().split(";")[2]

def column_mnemo():
    return content[i].strip().split(";")[3]   

def in_frase():
    return content[i].strip().split(";")[4]    

def frase_in_translate():
    return content[i].strip().split(";")[5]       

def the_whole_string():
    return content[i]   

def make_label(word,row,column):
    return label(frame=frame1,text=word,background="white",width=49,row=row,column=column)

def save_settings(arg):
    with open("lang_settings.txt", 'w', encoding="UTF-8") as f:
        f.write(arg)

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
        word = column_original_word()
        make_label(word+" "+column_transcription(),0,0) 
    except:
        #End of file
        make_label(interface["end_of_file"],0,0) 

    #clear line for the next word
    make_label("",1,0)  

    #Edit icons
    photo(frame=icons,file="icons/edit.png",row=0,column=0)
    photo_click().bind("<Button-1>",lambda url:edit_or_add_original_word())

    photo(frame=icons,file="icons/edit.png",row=1,column=0)
    photo_click().bind("<Button-1>",lambda url:edit_or_add_translate())    

def check_in_web():
    url="https://translate.yandex.com/?lang=en-ru&text="+column_original_word()
    webbrowser.open_new_tab(url)  

def show_in_frase(): 
    win=str(random.random())
    window_2 = {"name_of_frame":str(random.random()),"padx":5,"pady":5}
    config(window=win,frame=window_2,size="402x272+600+300",background="white")
    title(window=win,frame=window_2,text=interface['rules_read'])  
    bg_color = "#FFCC99"  
    label(window=win,frame=window_2,text=interface["original_frase"],background="white",row=0,column=0)
    text_area(window=win,frame=window_2,name="original area",height=5,width=48,row=1,column=0) 
    insert_text_area(name="original area",text=in_frase(),color = "black")

    label(window=win,frame=window_2,text=interface["frase_in_translation"],background="white",row=2,column=0)
    text_area(window=win,frame=window_2,name="translated area",height=5,width=48,row=3,column=0)    
    insert_text_area(name="translated area",text=frase_in_translate(),color = "black")  

    def save_frases():
        content[i] = column_original_word()+";"+column_transcription()+";"+column_translate()+";"+column_mnemo()+";"+get_info("original area").strip()+";"+get_info("translated area").strip()+"\n"
        save_to_file(content)    

    button(window=win,frame=window_2,text=interface["save"],command=save_frases,row=4,column=0)

#show translate
def translate():
    word = column_translate()
    make_label(word,1,0) 

def rules():
    win=str(random.random())
    window_2 = {"name_of_frame":str(random.random()),"padx":5,"pady":5}
    config(window=win,frame=window_2,size="545x495+600+200",background="white")
    title(window=win,frame=window_2,text=interface['rules_read'])
    with open(interface['rules_file'], encoding="UTF-8") as reader:
        text = reader.read()
    label(window=win,frame=window_2,text=text,background="white",
    width=58,height=25,wrap=500,justify="left",row=0,column=0)

def new_word():
    win=str(random.random())
    window_2 = {"name_of_frame":str(random.random()),"background":"white","padx":5,"pady":5}
    config(window=win,frame=window_2,size="345x350+600+300",background="white")  
    title(window=win,frame=window_2,text=interface["new_word"]) 
    bg_color = "#FFCC99"

    #original text area
    label(window=win,frame=window_2,text=interface["original_word"],background="white",row=0,column=0)
    entry(window=win,frame=window_2,name="entry original word",inner_border=4,background=bg_color,justify="center",row=1,column=0) 

    label(window=win,frame=window_2,text=interface["transcription"],background="white",row=2,column=0)
    entry(window=win,frame=window_2,name="entry transcription",inner_border=4,background=bg_color,justify="center",row=3,column=0)     

    #translate teat area
    label(window=win,frame=window_2,text=interface["translate"],background="white",row=4,column=0)
    text_area(window=win,frame=window_2,name="translate area",background=bg_color,inner_border=4,width=40,height=3,row=5,column=0)
    
    #mnemo phase - teat area
    label(window=win,frame=window_2,text=interface["mnemo_phrase"],background="white",row=6,column=0)
    text_area(window=win,frame=window_2,name="mnemoarea",background=bg_color,inner_border=4,width=40,height=4,row=7,column=0)

    def save_new_word():
        content = get_info("entry original word")+";"+get_info("entry transcription").strip()+";"+get_info("translate area").strip()+";"+get_info("mnemoarea").strip()+";"+in_frase()+";"+frase_in_translate()+"\n"

        with open(filename, 'a+', encoding="UTF-8") as file:
            file.write(content)    

        msg_box_warning("warning",interface["saved"])    
        quit(window=win)  

    button(window=win,frame=window_2,text=interface["save"],command=save_new_word,row=8,column=0)

def edit_or_add_original_word():
    global win
    win=str(random.random())
    frame_original = {"name_of_frame":str(random.random()),"padx":0,"pady":0}    
    config(window=win,frame=frame_original,size="393x295+600+300",background="white")
    title(window=win,text=interface["edit_original"])
    #Original
    label(window=win,frame=frame_original,text=interface["original_word"],background="#ccffcc",row=0,column=0)
    text_area(window=win,frame=frame_original,name="original area",height=5,width=48,row=1,column=0) 
    insert_text_area(name="original area",text=column_original_word(),color = "black")
    #Transcription
    label(window=win,frame=frame_original,text=interface["transcription"],background="#ccffcc",row=2,column=0)
    text_area(window=win,frame=frame_original,name="transcription area",height=5,width=48,row=3,column=0) 
    insert_text_area(name="transcription area",text=column_transcription(),color = "black")
    #Buttons

    def save_original():
        content[i] = get_info("original area").strip()+";"+get_info("transcription area").strip()+";"+column_translate()+";"+column_mnemo()+";"+in_frase()+";"+frase_in_translate()+"\n"
        save_to_file(content)

    button(window=win,frame=frame_original,text=interface["check_in_yandex"],command=check_in_web,row=4,column=0)
    button(window=win,frame=frame_original,text=interface["save"],command=save_original,row=5,column=0)

def edit_or_add_translate():
    global win
    win=str(random.random())
    frame_original = {"name_of_frame":str(random.random()),"padx":0,"pady":0}    
    config(window=win,frame=frame_original,size="392x177+600+300",background="white")    
    title(window=win,text=interface["edit_translate"])
    label(window=win,frame=frame_original,text=interface["edit_translate"],background="#ccffcc",row=0,column=0)
    text_area(window=win,frame=frame_original,name="translate area",height=5,width=48,row=1,column=0) 
    insert_text_area(name="translate area",text=column_translate(),color = "black")

    def save_translate():
        content[i] = column_original_word()+";"+column_transcription()+";"+get_info("translate area").strip()+";"+column_mnemo()+";"+in_frase()+";"+frase_in_translate()+"\n"
        save_to_file(content)    

    button(window=win,frame=frame_original,text=interface["check_in_yandex"],command=check_in_web,row=2,column=0)
    button(window=win,frame=frame_original,text=interface["save"],command=save_translate,row=3,column=0)    

def edit_or_add_memo():
    global win
    win=str(random.random())
    frame_original = {"name_of_frame":str(random.random()),"padx":0,"pady":0}    
    config(window=win,frame=frame_original,size="392x177+600+300",background="white")    
    title(window=win,text=interface["mneno_title"])
    label(window=win,frame=frame_original,text=interface["edit_mnemo"],background="#ccffcc",row=0,column=0)
    text_area(window=win,frame=frame_original,name="mnemo area",height=5,width=48,row=1,column=0) 
    insert_text_area(name="mnemo area",text=column_mnemo(),color = "black")

    def save_mnemo():
        content[i] = column_original_word()+";"+column_transcription()+";"+column_translate()+";"+get_info("mnemo area").strip()+";"+in_frase()+";"+frase_in_translate()+"\n"
        save_to_file(content)    

    button(window=win,frame=frame_original,text=interface["rules_of_mnenmo"],command=rules,row=2,column=0)
    button(window=win,frame=frame_original,text=interface["save"],command=save_mnemo,row=3,column=0)       

def delete_card():
    content[i] = ""
    save_to_file(content)    
    #restart_app()
    msg_box_warning("warning",interface["restart"])

def send_to_archive():
    content[i] = the_whole_string()
    with open("archive.csv", 'a+', encoding="UTF-8") as file:
        file.write(content[i])    
    delete_card()

def save_to_file(content):
    with open(filename, 'w', encoding="UTF-8") as file:
        for n in content:
            file.write(n)
    msg_box_warning("warning",interface["saved"])
    #quit(window=win)    

def save_direction(content):
    with open("direction.txt", 'w', encoding="UTF-8") as file:
        for n in content:
            file.write(n)    
    msg_box_warning("warning",interface["restart"])

def images():
    url="https://yandex.ru/images/search?text="+column_original_word()
    webbrowser.open_new_tab(url)   

start_settings()

#Empty screen on the start
make_label(interface["greetings"],0,0)
make_label("",1,0)

#Buttons
button(frame=buttons,text=interface["previous"],command=counter_minus,padx=5,pady=5,row=1,column=0)
button(frame=buttons,text=interface["next"],command=counter_plus,padx=5,pady=5,row=1,column=1)
button(frame=buttons,text=interface["mnemo_button"],command=edit_or_add_memo,padx=5,pady=5,row=1,column=2)
button(frame=buttons,text=interface["translate"],command=translate,padx=5,pady=5,row=1,column=3)

button(frame=buttons,text=interface["add_card"],command=new_word,padx=5,pady=5,row=2,column=0)
button(frame=buttons,text=interface["delete_card"],command=delete_card,padx=5,pady=5,row=2,column=1)
button(frame=buttons,text=interface["show in frase"],command=show_in_frase,padx=5,pady=5,row=2,column=2)
button(frame=buttons,text=interface["archive"],command=send_to_archive,padx=5,pady=5,row=2,column=3)

tabs = {interface["language"]:{"English":lambda:switch_to("english"),"Russian":lambda:switch_to("russian"),"---":"---","Exit":quit},
interface["directions"]:{"English -> Russian":lambda:save_direction("eng_rus.csv"),"Russian -> English":lambda:save_direction("rus_eng.csv")},
"Help":{"Help Index":"False","About...":"False","Help":"False"}}

top_menu(tabs)

app_loop()