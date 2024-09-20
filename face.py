#!/usr/bin/python3
# coding: utf-8

# ./face.py config.json

import os
import sys
from sys import argv
import json
import math
import subprocess
from tkinter import *
from tkinter import ttk

height = 700
weight = 700

root = Tk()

conf_path = argv[1]
config = {}
with open(conf_path, 'r') as json_file:
    config = json.load(json_file)

host = config['host']
port = config['port']

start = int(config['start'])
end = int(config['end'])
name = config['user_name']

command = "curl --header \"Content-Type: application/json\" --request PUT --data \'{\"start\": \""+str(start)+"\", \"end\": \""+str(end)+"\"}\' "+host+":"+port+"/set_range"
subprocess.check_output(command, shell=True)

class Window(Frame):  
    global start, end, name
    
    canvass = Canvas(width = weight, height = height, bg = 'lightgrey')
    
    canvass.create_line(weight/2, 0, weight/2,  height, width = 2, fill = 'black') # вниз
    canvass.create_line(0, height/2, weight, height/2, width = 2, fill = 'black')      # вбок
    
    Label(text = "Случайное число").place(x = 100 , y = 0)
    Label(text = "Диапазон случайного числа").place(x = 70 , y = weight/2 + 2)
    Label(text = "Любимое число ❤").place(x = height/2 + 100 , y = 0)
    Label(text = "История из последних 10ти чисел").place(x = height/2 + 60 , y = weight/2 + 2)
    
    text_edit_1 = Entry(width=5)
    text_edit_1.insert(0, '--------')
    text_edit_1.place(x = (height/2)/2 - 15 , y = (weight/2)/2 - 5)
    
    text_edit_21 = Entry(width=5)
    text_edit_21.insert(0, str(start))
    text_edit_21.place(x = (height/2)/2 - 150 , y = (weight - (weight/2)/2) - 5)
    
    text_edit_22 = Entry(width=5)
    text_edit_22.insert(0, str(end))
    text_edit_22.place(x = (height/2)/2 + 100 , y = (weight - (weight/2)/2) - 5)

    canvass.create_line(30, weight - (weight/2)/2 + 35, height/2 - 30, weight - (weight/2)/2 + 35, width = 2, fill = 'red') # вбок
    
    Label(text = "❤ :").place(x = height/2 + 120 , y = 175)
    text_edit_3 = Entry(width=5)
    text_edit_3.insert(0, '❤❤❤❤')
    text_edit_3.place(x = (height/2) + 155 , y = 175)
    

    def __init__(self):
        super().__init__()
        self.initUI() 
        
    def click1(event):  # функция вызываемая при нажатии на кнопку
        global name, host, port
        command = "curl -XGET "+host+":"+port+"/random/" + name
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        #data = json.dumps(str(result)) # dict to string
        data = json.loads(result) # string to json
        val = data["value"]
        Window.text_edit_1.delete(0, END)
        Window.text_edit_1.insert(0, str(val))
        
        
    def click2(event):  # функция вызываемая при нажатии на кнопку
        global name, start, end, host, port
        start = Window.text_edit_21.get()
        end = Window.text_edit_22.get()
        if (int(end) > int(start)):
            command = "curl --header \"Content-Type: application/json\" --request PUT --data \'{\"start\": \""+str(start)+"\", \"end\": \""+str(end)+"\"}\' "+host+":"+port+"/set_range"
            subprocess.check_output(command, shell=True)
        else:
            print('Начало диапазона чисел должно быть больше конца диапазона')
        
    def click3(event):  # функция вызываемая при нажатии на кнопку
        global name, host, port
        command = "curl -XGET "+host+":"+port+"/love/" + name
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        #data = json.dumps(str(result)) # dict to string
        data = json.loads(result) # string to json
        val = data["love"]
        val = str(val).replace('[(', '').replace(',)]', '')
        Window.text_edit_3.delete(0, END)
        Window.text_edit_3.insert(0, str(val))
        
    def click4(event):  # функция вызываемая при нажатии на кнопку
        global name, host, port
        command = "curl -XGET "+host+":"+port+"/history/" + name
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        #data = json.dumps(str(result)) # dict to string
        data = json.loads(result) # string to json
        val = data["history"]
        i = 1
        for elem in val:
            Label(text = str(i)+":").place(x = height/2 + 120 , y = height/2 + 50 + 20*(i))
            Label(text = str(elem[0])).place(x = height/2 + 150 , y = height/2 + 50 + 20*(i))
            i = i + 1
    
    def initUI(self):
        self.master.title("Random")
        self.pack(fill=BOTH, expand=1)
        
        canvas = self.canvass

        but_1 = Button(text='Получить',  # Создаем кнопку и присваиваем ее в переменную
               width=42, height=1,  # Устанавливаем размер кнопки
               bg='#C4C4C4', fg='black',  # цвет фона и надписи
               activebackground='#CFCFCF',  # цвет нажатой кнопки
               activeforeground='#383838',  # цвет надписи когда кнопка нажата
               font='Hack 8')  # устанавливаем шрифт и размер надписи
        but_1.bind('<Button-1>', Window.click1)  # Обработчик событий
        but_1.place(x = 10 , y = weight/2 - 30)
        
        but_2 = Button(text='Установить',  # Создаем кнопку и присваиваем ее в переменную
               width=42, height=1,  # Устанавливаем размер кнопки
               bg='#C4C4C4', fg='black',  # цвет фона и надписи
               activebackground='#CFCFCF',  # цвет нажатой кнопки
               activeforeground='#383838',  # цвет надписи когда кнопка нажата
               font='Hack 8')  # устанавливаем шрифт и размер надписи
        but_2.bind('<Button-1>', Window.click2)  # Обработчик событий
        but_2.place(x = 10 , y = weight - 30)
        
        but_3 = Button(text='Узнать ❤',  # Создаем кнопку и присваиваем ее в переменную
               width=42, height=1,  # Устанавливаем размер кнопки
               bg='#C4C4C4', fg='black',  # цвет фона и надписи
               activebackground='#CFCFCF',  # цвет нажатой кнопки
               activeforeground='#383838',  # цвет надписи когда кнопка нажата
               font='Hack 8')  # устанавливаем шрифт и размер надписи
        but_3.bind('<Button-1>', Window.click3)  # Обработчик событий
        but_3.place(x = height/2 + 10 , y = weight/2 - 30)
        
        but_4 = Button(text='Посмотреть',  # Создаем кнопку и присваиваем ее в переменную
               width=42, height=1,  # Устанавливаем размер кнопки
               bg='#C4C4C4', fg='black',  # цвет фона и надписи
               activebackground='#CFCFCF',  # цвет нажатой кнопки
               activeforeground='#383838',  # цвет надписи когда кнопка нажата
               font='Hack 8')  # устанавливаем шрифт и размер надписи
        but_4.bind('<Button-1>', Window.click4)  # Обработчик событий
        but_4.place(x = height/2 + 10 , y = weight - 30)
        
        canvas.pack(fill=BOTH, expand=1) 
def main():
    global root, height, weight
    face = Window()
    root.geometry(str(height)+'x'+str(weight))
    root.mainloop()

if __name__ == '__main__':
    main()
