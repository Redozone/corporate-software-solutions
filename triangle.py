#!/usr/bin/python3
# coding: utf-8

import os
import sys
from sys import argv
import json
import math
#import numpy
from tkinter import * #Tk, Canvas, Frame, BOTH
from tkinter import ttk

config = {}

def read_config():
    global config
    with open('config.json', 'r') as config_file:
        obj=config_file.read()
    config = json.loads(obj)

read_config()

def write_config():
   global config
   with open('config.json', 'w', encoding='utf-8') as outfile:
       json.dump(config, outfile, ensure_ascii=False, indent=4)

h = float(config["suspension_height"])   # высота подвеса
l = float(config["platform_length"])     # длина площадки
e = float(config["start_of_the_scene"])  # начало сцены (первые слушатели)
elems = int(config["elements"])          # кол-во элементов
h_sound = float(config["sound_height"])  # высота колонки
max_range = float(config["max_range"])   # максимальная дальность озвучки

step = (l - e) / elems

selection = ""
selection_metods = ""

list_angels = []

def start_triangle(h, l):
    hypotenuse = round(math.sqrt( h**2 + l**2), 5)
    sin_a = round(h/hypotenuse, 5)
    triangle_a = round(math.degrees(math.asin(sin_a)), 5)
    return triangle_a

def jump(h_sound, triangle):
    triangleA = 90 - triangle
    l2 = h_sound * math.sin(math.radians(triangleA))
    return l2
    
def jump_left(h_sound, triangle):
    l2_left = h_sound * math.sin(math.radians(triangle))
    return l2_left
    
# -------------------------------------------------------------------
# линейный способ
# -------------------------------------------------------------------

list_x = []
y = 0
h_dubler = h
list_y = []
list_l = []

def linear_formul():

    global h, l, e, elems, h_sound, max_range, step, list_angels, list_x, y, h_dubler, list_y, list_l, selection, selection_metods
    for i in range(elems+1, 0, -1):
        triangl_step = start_triangle(h, l)
    
        list_x.append(h_dubler)
        #print(list_x)
        list_y.append(y)
        list_l.append(l)
    
        if i == elems+1:
            list_angels.append(triangl_step)
            new_h1 = round(jump(h_sound, triangl_step), 5)
            new_h2 = round(jump(h_sound,triangl_step), 5)
            y_step = round(jump_left(h_sound, triangl_step), 5)
            #print('new_h_1', triangl_step, new_h1, h)
        else:
            #list_angels.append(round(triangl_step - list_angels[len(list_angels) - 1], 5))
            new_h2 = round(jump(h_sound,triangl_step), 5)
            new_h1 = round(jump(h_sound, round(triangl_step - sum(list_angels), 5)), 5)
            y_step = round(jump_left(h_sound, triangl_step), 5) #round(jump_left(h_sound, triangl_step - sum(list_angels)), 5)
            #print('new_h',round(triangl_step - sum(list_angels), 5), new_h1, h)
            list_angels.append(round(triangl_step - sum(list_angels), 5))

        
        y = y - y_step
        h_dubler = h_dubler - new_h2    
        h = h - new_h1
        l = l - step
        #if i == 0:
        #    list_x.append(h)
        #    list_y.append(y)
        #    list_l.append(l) 
    
    print('Результаты линейного способа')
    print(list_angels[:-1])
    for k in range(0, len(list_angels)-1):
        if k == 0:
            print("Угол подвеса рамы (равен углу первого элемента массива):    " + str(list_angels[k]) + '°')
        else:
            print('Угол подвеса ' + str(k+1) + ' элемента массива (относительно предыдущего): ' + str(list_angels[k]) + '°')
        
    
# -------------------------------------------------------------------
# другой способ (деление на 3)
# -------------------------------------------------------------------
    
h = float(config["suspension_height"])   # высота подвеса
l = float(config["platform_length"])     # длина площадки
e = float(config["start_of_the_scene"])  # начало сцены (первые слушатели)
elems = int(config["elements"])          # кол-во элементов
h_sound = float(config["sound_height"])  # высота колонки    


list_x2 = []
y = 0
h_dubler2 = h
list_y2 = []
list_l2 = []
list_angels_another = []
    
#for i in range(elems, 0, -1):  

def division_by_three():
    global h, l, e, elems, h_sound, max_range, step, list_angels, list_x, y, h_dubler, list_y, list_l, selection, selection_metods
    global list_x2, y, h_dubler2, list_y2, list_l2, list_angels_another
    allocation = elems % 3

    list_angels_another = []
    if allocation == 0:
        zones_count = 3
        elements_in_zone = elems / zones_count
        count_elems_in_zones = []
        for i in range(0, 3):
            count_elems_in_zones.append(int(elements_in_zone))
    
        for k in range(0, zones_count):    
            step = ((float(config["platform_length"]) - e) / 3) / count_elems_in_zones[k] 
            #list_x2.append(h_dubler2)
            #list_y2.append(y)
            #list_l2.append(l) 
            elem_u_count = int(count_elems_in_zones[k])  
            if k == 2:
                elem_u_count = elem_u_count + 1
            for j in range(0, elem_u_count):
                list_x2.append(h_dubler2)
                #print(list_x2)
                list_y2.append(y)
                list_l2.append(l) 
                traingl_set = start_triangle(h, l)
                if 0 == len(list_angels_another):
                    list_angels_another.append(traingl_set)
                    new_h1 = round(jump(h_sound, traingl_set), 5)
                    new_h2 = round(jump(h_sound,traingl_set), 5)
                    y_step = round(jump_left(h_sound, traingl_set), 5)
                    #print('new_h_1', traingl_set, new_h1, h)
                else:
                    new_h1 = round(jump(h_sound, round(traingl_set - sum(list_angels_another), 5)), 5)
                    new_h2 = round(jump(h_sound,traingl_set), 5)
                    #print('new_h', round(traingl_set - sum(list_angels_another), 5), new_h1, h)
                    y_step = round(jump_left(h_sound, traingl_set), 5)
                    list_angels_another.append(round(traingl_set - sum(list_angels_another), 5))
                y = y - y_step
                h_dubler2 = h_dubler2 - new_h2    
                h = h - new_h1
                l = l - step
            

    if allocation == 1:
        zones_count = 3
        min_elem = (elems - 1) / zones_count
        count_elems_in_zones = [min_elem + 1, min_elem, min_elem]
            
        for k in range(0, zones_count):    
            step = ((float(config["platform_length"]) - e) / 3) / count_elems_in_zones[k]  
            elem_u_count = int(count_elems_in_zones[k])  
            if k == 2:
                elem_u_count = elem_u_count + 1 
                 
            for j in range(0, elem_u_count):
                traingl_set = start_triangle(h, l)
                list_x2.append(h_dubler2)
                list_y2.append(y)
                list_l2.append(l) 
                if 0 == len(list_angels_another):
                    list_angels_another.append(traingl_set)
                    new_h1 = round(jump(h_sound, traingl_set), 5)
                    new_h2 = round(jump(h_sound,traingl_set), 5)
                    y_step = round(jump_left(h_sound, traingl_set), 5)
                    #print('new_h_1', traingl_set, new_h1, h)
                else:
                    new_h1 = round(jump(h_sound, round(traingl_set - sum(list_angels_another), 5)), 5)
                    new_h2 = round(jump(h_sound,traingl_set), 5)
                    #print('new_h', round(traingl_set - sum(list_angels_another), 5), new_h1, h)
                    y_step = round(jump_left(h_sound, traingl_set), 5)
                    list_angels_another.append(round(traingl_set - sum(list_angels_another), 5))
                y = y - y_step
                h_dubler2 = h_dubler2 - new_h2 
                h = h - new_h1
                l = l - step


    if allocation == 2:
        zones_count = 3
        min_elem = (elems - 2) / zones_count
        count_elems_in_zones = [min_elem + 1, min_elem + 1, min_elem]

        for k in range(0, zones_count):    
            step = ((float(config["platform_length"]) - e) / 3) / count_elems_in_zones[k]  
            elem_u_count = int(count_elems_in_zones[k])  
            if k == 2:
                elem_u_count = elem_u_count + 1 
                 
            for j in range(0, elem_u_count):
                traingl_set = start_triangle(h, l)
                list_x2.append(h_dubler2)
                list_y2.append(y)
                list_l2.append(l) 
                if 0 == len(list_angels_another):
                    list_angels_another.append(traingl_set)
                    new_h1 = round(jump(h_sound, traingl_set), 5)
                    new_h2 = round(jump(h_sound,traingl_set), 5)
                    y_step = round(jump_left(h_sound, traingl_set), 5)
                    #print('new_h_1', traingl_set, new_h1, h)
                else:
                    new_h1 = round(jump(h_sound, round(traingl_set - sum(list_angels_another), 5)), 5)
                    new_h2 = round(jump(h_sound,traingl_set), 5)
                    #print('new_h', round(traingl_set - sum(list_angels_another), 5), new_h1, h)
                    y_step = round(jump_left(h_sound, traingl_set), 5)
                    list_angels_another.append(round(traingl_set - sum(list_angels_another), 5))
                y = y - y_step
                h_dubler2 = h_dubler2 - new_h2 
                h = h - new_h1
                l = l - step
            
        
    print('\n\n\n')        
    print('Результаты способа деления на 3')
    print(list_angels_another[:-1])
    for k in range(0, len(list_angels_another)-1):
        if k == 0:
            print("Угол подвеса рамы (равен углу первого элемента массива):    " + str(list_angels_another[k]) + '°')
        else:
            print('Угол подвеса ' + str(k+1) + ' элемента массива (относительно предыдущего): ' + str(list_angels_another[k]) + '°')           
        
        
# РИСОВАНИЕ
# https://python-scripts.com/tkinter-canvas-example
# https://dzen.ru/a/XvTC2P9GCjCrJ0KC?utm_referer=www.yandex.ru

root = Tk()
'''
def click(event):  # функция вызываемая при нажатии на кнопку
        print('Вы нажали на кнопку')
        Example.formuls()
'''
height = 700
weight = 700

class Example(Frame):
    global h, l, e, elems, h_sound, max_range, step, list_angels, list_x, y, h_dubler, list_y, list_l, config, selection, selection_metods
    canvass = Canvas(width = weight, height = height, bg = 'lightgrey') #Canvas(self)
    
    Label(text = 'h подвеса, м.').place(x = weight - 235, y = 39)
    text_edit_h = Entry(width=5) #Text(width=10 , height=1)
    text_edit_h.insert(0, str(config["suspension_height"]))
    text_edit_h.place(x = weight - 50 , y = 39)

    Label(text = 'последний зритель, м.').place(x = weight - 235, y = 61)
    text_edit_l = Entry(width=5)
    text_edit_l.insert(0, str(config["platform_length"]))
    text_edit_l.place(x = weight - 50 , y = 61)
    
    Label(text = 'первый зритель, м.').place(x = weight - 235, y = 82)
    text_edit_e = Entry(width=5)
    text_edit_e.insert(0, str(config["start_of_the_scene"]))
    text_edit_e.place(x = weight - 50 , y = 82)
    
    Label(text = 'количество элементов').place(x = weight - 235, y = 103)
    text_edit_elem = Entry(width=5)
    text_edit_elem.insert(0, str(config["elements"]))
    text_edit_elem.place(x = weight - 50 , y = 103)
    
    sounds_names = list(config["sound_list"])
    combobox = ttk.Combobox(values=sounds_names)
    combobox.place(x = weight - 235 , y = 124)
    combobox.set(sounds_names[0])
    selection = sounds_names[0]
    
    def selected(event):
        global h, l, e, elems, h_sound, max_range, step, list_angels, list_x, y, h_dubler, list_y, list_l, config, selection
        global list_x2, y, h_dubler2, list_y2, list_l2, list_angels_another 
        # получаем выделенный элемент
        selection = Example.combobox.get()
    
    combobox.bind("<<ComboboxSelected>>", selected)
    
    metods = ["Линейный метод", "Деление на три"]
    combobox_metods = ttk.Combobox(values=metods)
    combobox_metods.place(x = weight - 235 , y = 145)
    combobox_metods.set(metods[0])
    selection_metods = metods[0]
    
    def selected_metods(event):
        global h, l, e, elems, h_sound, max_range, step, list_angels, list_x, y, h_dubler, list_y, list_l, config, selection, selection_metods
        global list_x2, y, h_dubler2, list_y2, list_l2, list_angels_another 
        # получаем выделенный элемент
        selection_metods = Example.combobox_metods.get()
        
    combobox_metods.bind("<<ComboboxSelected>>", selected_metods)
    
    def __init__(self):
        super().__init__()
        self.initUI()  
        
    def click(event):  # функция вызываемая при нажатии на кнопку
        global h, l, e, elems, h_sound, max_range, step, list_angels, list_x, y, h_dubler, list_y, list_l, config, selection, selection_metods
        global list_x2, y, h_dubler2, list_y2, list_l2, list_angels_another      
        
        text_h = Example.text_edit_h.get()
        text_l = Example.text_edit_l.get()
        text_e = Example.text_edit_e.get()
        text_elem = Example.text_edit_elem.get()  #(0.3,END)

        config["suspension_height"] = text_h
        config["platform_length"] = text_l
        config["start_of_the_scene"] = text_e
        # проверка что элементов больше 2х для способа деления на три
        config["elements"] = text_elem
        write_config()
        read_config()
        h = float(config["suspension_height"])   # высота подвеса
        l = float(config["platform_length"])     # длина площадки
        e = float(config["start_of_the_scene"])  # начало сцены (первые слушатели)
        elems = int(config["elements"])          # кол-во элементов
        map_sound = {}
        map_cound = config[selection]
        h_sound = float(map_cound["sound_height"])  # высота колонки
        max_range = float(map_cound["max_range"])   # максимальная дальность озвучки
        step = (l - e) / elems
        
        
        
        
       # h = float(config["suspension_height"])   # высота подвеса
        #l = float(config["platform_length"])     # длина площадки
        #e = float(config["start_of_the_scene"])  # начало сцены (первые слушатели)
        #elems = int(config["elements"])          # кол-во элементов
        
        

        #canvass.delete("all")
        if selection_metods == "Линейный метод":
            print(selection_metods)
            list_x = []
            y = 0
            h_dubler = h
            list_y = []
            list_l = []
            
            list_angels = []
            
            linear_formul()
            Example.formuls(Example.canvass, 1) 
        if selection_metods == "Деление на три":
            print(selection_metods)
            list_x2 = []
            y = 0
            h_dubler2 = h
            list_y2 = []
            list_l2 = []
            list_angels_another = []
            
            division_by_three()
            Example.formuls(Example.canvass, 2) 
         
        
            
        
    def formuls(canvas, id):
        global h, l, e, elems, h_sound, max_range, step, list_angels, list_x, y, h_dubler, list_y, list_l, config, selection
        global list_x2, y, h_dubler2, list_y2, list_l2, list_angels_another
        canvas.delete(ALL)
        
        #canvas = self.canvass
        canvas.create_line(weight - 240, 0, weight - 240,  175, width = 2, fill = 'black') # вниз
        canvas.create_line(weight - 240, 175, weight, 175, width = 2, fill = 'black')      # вбок
        canvas.create_line(0, height*0.5, weight, height*0.5, width = 2, fill = 'red') # разделительная
        canvas.create_line(30, height*0.5 - 50, weight - 30, height*0.5 - 50) # пол
        
        type_formul = id
        
        # проверка на максимальную длину (выход за пределы)
        shift = float(config["platform_length"])
        shift_up = (weight-30)/float(config["platform_length"])
        if float(config["platform_length"]) > max_range:
            shift = shift * max_range/float(config["platform_length"]) # float(config["platform_length"]) * 100 / max_range;  

        # линии направления 
        # отрисовка по линейной формуле
        
        
        if type_formul == 1:
            for i in range(0, len(list_x)-1):
                #canvas.create_line(60 + round(list_y[i], 3)*300, height*0.5 - 150 - round(list_x[i], 3)*30, (weight - 35)*round((list_l[i]/shift), 3), height*0.5 - 50, activefill = 'pink')
                canvas.create_line(30 + round(list_y[i], 3)*shift_up, height*0.5 - 50 - round(list_x[i], 3)*shift_up, (weight - 30)*round((list_l[i]/shift), 3), height*0.5 - 50, activefill = 'green')
                
            
            # подписи длин и расположение элементов
            Label(text = '', width = weight).place(x = 0, y = height*0.5 - 40) # идет какой то дубляж (сохранение старых) цыфр, просто затираем это поле
            for i in range(0, len(list_x)):
                Label(text = str(round(list_l[i], 1))).place(x = (weight - 50)*(list_l[i]/shift), y = height*0.5 - 40)
                try:
                    #canvas.create_line(60 + round(list_y[i], 3)*300, height*0.5 - 150 - round(list_x[i], 3)*30, 60 + round(list_y[i+1], 3)*300, height*0.5 - 150 - round(list_x[i+1], 3)*30, activefill = 'pink')
                    canvas.create_line(30 + round(list_y[i], 3)*shift_up, height*0.5 - 50 - round(list_x[i], 3)*shift_up,
                     30 + round(list_y[i+1], 3)*shift_up, height*0.5 - 50 - round(list_x[i+1], 3)*shift_up, activefill = 'green')

                except:
                    pass
                    
                   
            # текс углов    
            down = 20
            Label(text = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', width = 80).place(x = 30, y = height*0.5 + 15) # очиститель поля углов
            for k in range(0, len(list_angels)-1):
                if k == 0:
                    Label(text = "Угол подвеса рамы (равен углу первого элемента массива):      " + str(list_angels[k]) + '°').place(x = 30 , y = weight*0.5 + down)
                else:
                    Label(text = 'Угол подвеса ' + str(k+1) + ' элемента массива (относительно предыдущего): ' + str(list_angels[k]) + '°').place(x = 30 , y = weight*0.5 + down)
            
                down = down + 20
                
            print('======================================================')
            
        
        # отрисовка по формуле деления на 3    
        if type_formul == 2: # пока не работает    
                  
            for i in range(0, len(list_x2)-1):
                canvas.create_line(30 + round(list_y2[i], 3)*shift_up, height*0.5 - 50 - round(list_x2[i], 3)*shift_up, (weight - 30)*round((list_l2[i]/shift), 3), height*0.5 - 50, activefill = 'green')
                
            
            # подписи длин и расположение элементов
            Label(text = '', width = weight).place(x = 0, y = height*0.5 - 40) # идет какой то дубляж (сохранение старых) цыфр, просто затираем это поле
            for i in range(0, len(list_x2)):
                Label(text = str(round(list_l2[i], 1))).place(x = (weight - 50)*(list_l2[i]/shift), y = height*0.5 - 40)
                try:
                    canvas.create_line(30 + round(list_y2[i], 3)*shift_up, height*0.5 - 50 - round(list_x2[i], 3)*shift_up,
                     30 + round(list_y2[i+1], 3)*shift_up, height*0.5 - 50 - round(list_x2[i+1], 3)*shift_up, activefill = 'green')

                except:
                    pass
                               
            # текс углов    
            down = 20
            Label(text = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', width = 80).place(x = 30, y = height*0.5 + 15) # очиститель поля углов
            for k in range(0, len(list_angels_another)-1):
                if k == 0:
                    Label(text = "Угол подвеса рамы (равен углу первого элемента массива):      " + str(list_angels_another[k]) + '°').place(x = 30 , y = weight*0.5 + down)
                else:
                    Label(text = 'Угол подвеса ' + str(k+1) + ' элемента массива (относительно предыдущего): ' + str(list_angels_another[k]) + '°').place(x = 30 , y = weight*0.5 + down)
            
                down = down + 20
                
            print('======================================================')
        
    def initUI(self):
        self.master.title("Рисуем линии")
        self.pack(fill=BOTH, expand=1)
        
        canvas = self.canvass

        #canvas = Canvas(width = weight, height = height, bg = 'lightgrey') #Canvas(self)
        
        #canvas.create_line(0, 0, 500, 0) # параллельная
        #canvas.create_line(0, 0, 0, 500) # перпендикулярная
        #canvas.create_line(0, 0, 500, 500) # лево верх это 0;0
        
        canvas.create_line(0, height*0.5, weight, height*0.5, width = 2, fill = 'red') # разделительная
        
        canvas.create_line(30, height*0.5 - 50, weight - 30, height*0.5 - 50) # пол
        
        canvas.create_line(weight - 240, 0, weight - 240,  175, width = 2, fill = 'black') # вниз
        canvas.create_line(weight - 240, 175, weight, 175, width = 2, fill = 'black')      # вбок
        
        but_1 = Button(text='Расчитать',  # Создаем кнопку и присваиваем ее в переменную
               width=14, height=1,  # Устанавливаем размер кнопки
               bg='#C4C4C4', fg='black',  # цвет фона и надписи
               activebackground='#CFCFCF',  # цвет нажатой кнопки
               activeforeground='#383838',  # цвет надписи когда кнопка нажата
               font='Hack 16')  # устанавливаем шрифт и размер надписи
        but_1.bind('<Button-1>', Example.click)  # Обработчик событий
        but_1.place(x = weight - 230 , y = 0)
        
        type_formul = 1 # delete
        '''
        type_formul = 1
        
        # проверка на максимальную длину (выход за пределы)
        shift = float(config["platform_length"])
        shift_up = (weight-30)/float(config["platform_length"])
        if float(config["platform_length"]) > max_range:
            shift = shift * max_range/float(config["platform_length"]) # float(config["platform_length"]) * 100 / max_range;  
        
        # линии направления
        if type_formul == 1:
            for i in range(0, len(list_x)-1):
                #canvas.create_line(60 + round(list_y[i], 3)*300, height*0.5 - 150 - round(list_x[i], 3)*30, (weight - 35)*round((list_l[i]/shift), 3), height*0.5 - 50, activefill = 'pink')
                canvas.create_line(30 + round(list_y[i], 3)*shift_up, height*0.5 - 50 - round(list_x[i], 3)*shift_up, (weight - 30)*round((list_l[i]/shift), 3), height*0.5 - 50, activefill = 'green')
                
        
            # подписи длин и расположение элементов
            for i in range(0, len(list_x)):
                Label(text = str(round(list_l[i], 1))).place(x = (weight - 50)*(list_l[i]/shift), y = height*0.5 - 40)
                try:
                    #canvas.create_line(60 + round(list_y[i], 3)*300, height*0.5 - 150 - round(list_x[i], 3)*30, 60 + round(list_y[i+1], 3)*300, height*0.5 - 150 - round(list_x[i+1], 3)*30, activefill = 'pink')
                    canvas.create_line(30 + round(list_y[i], 3)*shift_up, height*0.5 - 50 - round(list_x[i], 3)*shift_up,
                     30 + round(list_y[i+1], 3)*shift_up, height*0.5 - 50 - round(list_x[i+1], 3)*shift_up, activefill = 'green')

                except:
                    pass
            
            # текс углов    
            down = 20        
            for k in range(0, len(list_angels)-1):
                if k == 0:
                    Label(text = "Угол подвеса рамы (равен углу первого элемента массива):      " + str(list_angels[k]) + '°').place(x = 30 , y = weight*0.5 + down)
                else:
                    Label(text = 'Угол подвеса ' + str(k+1) + ' элемента массива (относительно предыдущего): ' + str(list_angels[k]) + '°').place(x = 30 , y = weight*0.5 + down)
            
                down = down + 20
                
        '''
        '''
        if type_formul == 2: # пока не работает 
            for i in range(0, len(list_x2)-1):
                canvas.create_line(60 + round(list_y2[i], 3)*300, height*0.5 - 150 - round(list_x2[i], 3)*30, (weight - 35)*round((list_l2[i]/100), 3), height*0.5 - 50, activefill = 'green')
        
            for i in range(0, len(list_x2)):
                Label(text = str(list_l2[i])).place(x = (weight - 50)*(list_l2[i]/100), y = height*0.5 - 40)
                try:
                    canvas.create_line(60 + round(list_y2[i], 3)*300, height*0.5 - 150 - round(list_x2[i], 3)*30, 60 + round(list_y2[i+1], 3)*300, height*0.5 - 150 - round(list_x2[i+1], 3)*30, activefill = 'green')
                except:
                    pass
                
            down = 20        
            for k in range(0, len(list_angels_another)-1):
                if k == 0:
                    Label(text = "Угол подвеса рамы (равен углу первого элемента массива):      " + str(list_angels_another[k]) + '°').place(x = 30 , y = weight*0.5 + down)
                else:
                    Label(text = 'Угол подвеса ' + str(k+1) + ' элемента массива (относительно предыдущего): ' + str(list_angels_another[k]) + '°').place(x = 30 , y = weight*0.5 + down)
            
                down = down + 20
            
        '''
        canvas.pack(fill=BOTH, expand=1) 
        
        
def main():
    #root = Tk()
    global root
    ex = Example()
    root.geometry(str(height)+'x'+str(weight))
    root.mainloop()
    
if __name__ == '__main__':
    main()        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
   
