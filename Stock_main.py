from os import getlogin
import kivy
import os
import math
import weakref
import pickle
from kivy import clock
from kivy.app import App
from kivy.uix.behaviors import button
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import RoundedRectangle,Color
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.utils import interpolate
from kivy.clock import Clock
from stock import *

categories = ['เนื้อสัตว์','ผัก','อาหารทานเล่น','เครื่องดื่ม','ผลไม้','น้ำซุป','ของหวาน', 'น้ำจิ้ม','อื่นๆ']


Config.set('graphics', 'width', '1440')
Config.set('graphics', 'height', '1024')


filesize = os.path.getsize("stock.pkl")
if filesize == 0:
    print(filesize,"print(filesize)1111")
    isCreatedStock = False
else:
    print(filesize,"print(filesize)2222")
    isCreatedStock = True

if isCreatedStock:
    s = loadStock()
else:
    s = Stock('Stock')
    for category in categories:
        s.addCategory(category)
        print(s.getDisplayItem(),55)

ref_dict={}
cat_dict = {}

def bubbleSort(arr):
    n = len(arr)
 
    # Traverse through all array elements
    for i in range(n):
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j][2] > arr[j+1][2] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

def get_len(category):
    if s.getCategory(category).getDisplayItem() == None:
        return 0
    return len(s.getCategory(category).getDisplayItem())

class MainWindow(Screen):
    item = ObjectProperty(None)

    def Btn(self):
        print("Search: ",self.item.text)

    def saveExit(self):
        saveStock(s)
        print('save&exit func...')
    
    def on_kv_post(self, obj):
        for i in categories:
            if s.getCategory(i).getDisplayItem() != None:
                for j in range(get_len(i)):
                    name = s.getCategory(i).getDisplayItem()[j][0]
                    s.getCategory(i).getType(name).updateRemainingExpHour()

        showlists = s.getDisplayItem()
        bubbleSort(showlists)
        print(showlists)
        showlists.insert(0,["ชื่อวัตถุดิบ","จำนวนคงเหลือ","เวลาคงเหลือ (ชั่วโมง)"])
        n = math.ceil(len(showlists))
        print("testtttttttttt")
        self.ids.showlists.height = (40*(n+1)+70*n)

        for i in range(len(showlists)):
            if showlists[i][2] != "เวลาคงเหลือ (ชั่วโมง)" and float("{:.4f}".format(float(showlists[i][2]))) <= 0:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                expire = Label(text='0.0000', font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])

            else:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                if showlists[i][2] == "เวลาคงเหลือ (ชั่วโมง)" :
                    expire = Label(text=str(showlists[i][2]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                else:
                    expire = Label(text=str("{:.4f}".format(float(showlists[i][2]))), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')

            self.ids.showlists.add_widget(label)
            self.ids.showlists.add_widget(amount)
            self.ids.showlists.add_widget(expire)
        Clock.schedule_interval(self.refresh,1)

    def refresh(self, *args):
        print("update realtime")
        self.ids.showlists.clear_widgets()
        for i in categories:
            if s.getCategory(i).getDisplayItem() != None:
                for j in range(get_len(i)):
                    name = s.getCategory(i).getDisplayItem()[j][0]
                    s.getCategory(i).getType(name).updateRemainingExpHour()

        showlists = s.getDisplayItem()
        bubbleSort(showlists)
        showlists.insert(0,["ชื่อวัตถุดิบ","จำนวนคงเหลือ","เวลาคงเหลือ (ชั่วโมง)"])

        n = math.ceil(len(showlists))
        self.ids.showlists.height = (40*(n+1)+70*n)

        for i in range(len(showlists)):
            if showlists[i][2] != "เวลาคงเหลือ (ชั่วโมง)" and float("{:.4f}".format(float(showlists[i][2]))) <= 0:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                expire = Label(text=str("0.0000"), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])

            else:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                if showlists[i][2] == "เวลาคงเหลือ (ชั่วโมง)" :
                    expire = Label(text=str(showlists[i][2]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                else:
                    expire = Label(text=str("{:.4f}".format(float(showlists[i][2]))), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')

            self.ids.showlists.add_widget(label)
            self.ids.showlists.add_widget(amount)
            self.ids.showlists.add_widget(expire)

class AddWindow(Screen):
    def on_kv_post(self, obj):
        n = math.ceil(len(categories)/3)
        self.ids.SV.height = (40*(n-1)+190*(n))
        # loop create categories BTN.
        for i in range(len(categories)):
            button = Button(text=categories[i], font_name='fonts/THSarabun Bold.ttf', font_size = 36, size_hint_y = None, height = 190)
            button.bind(on_press=self.pressed)
            self.ids[categories[i]] = weakref.ref(button)

            self.ids.BL1.add_widget(button)
    
    def back(self):
        print("Button on click: back main")
        self.manager.current = 'main'
        self.manager.current_screen.ids.showlists.clear_widgets()

        for i in categories:
            if s.getCategory(i).getDisplayItem() != None:
                for j in range(get_len(i)):
                    name = s.getCategory(i).getDisplayItem()[j][0]
                    s.getCategory(i).getType(name).updateRemainingExpHour()

        showlists = s.getDisplayItem()
        bubbleSort(showlists)
        showlists.insert(0,["ชื่อวัตถุดิบ","จำนวนคงเหลือ","เวลาคงเหลือ (ชั่วโมง)"])

        n = math.ceil(len(showlists))
        self.manager.current_screen.ids.showlists.height = (40*(n+1)+70*n)

        for i in range(len(showlists)):
            if showlists[i][2] != "เวลาคงเหลือ (ชั่วโมง)" and float("{:.4f}".format(float(showlists[i][2]))) <= 0:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                expire = Label(text=str("0.0000"), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])

            else:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                if showlists[i][2] == "เวลาคงเหลือ (ชั่วโมง)" :
                    expire = Label(text=str(showlists[i][2]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                else:
                    expire = Label(text=str("{:.4f}".format(float(showlists[i][2]))), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')

            self.manager.current_screen.ids.showlists.add_widget(label)
            self.manager.current_screen.ids.showlists.add_widget(amount)
            self.manager.current_screen.ids.showlists.add_widget(expire)

        

    def pressed(self, instance):
        print("Button on click:", instance.text)
        cat_dict['stayAt'] = instance.text
        # print(instance.text)
        self.manager.current = 'categories'
        self.manager.current_screen.ids.titleTXT.text = instance.text

        # generate widget.
        n = get_len(cat_dict['stayAt'])+1/1
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n) # กำหนดช่วงความสูงของ GridLayout ใน ScrollView
        label = Label(text='ชื่อวัตถุดิบ', font_size=24, size_hint_y=None, height=40,font_name='fonts/THSarabun Bold.ttf')
        amount = Label(text='จำนวน', font_size=24, size_hint_x=0.1, size_hint_y=None, height=40,font_name='fonts/THSarabun Bold.ttf')
        add = Label(text="", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        decrease = Label(text="", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        clear = Label(text=" ", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        reset = Label(text=" ", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        total = Label(text = str('คงเหลือ'), font_size=24, size_hint_y=None, height=40, size_hint_x=0.1,font_name='fonts/THSarabun Bold.ttf')
                
        # Add widget.
        self.manager.current_screen.ids.GL.add_widget(clear)
        self.manager.current_screen.ids.GL.add_widget(reset)
        self.manager.current_screen.ids.GL.add_widget(label)
        self.manager.current_screen.ids.GL.add_widget(decrease)
        self.manager.current_screen.ids.GL.add_widget(amount)
        self.manager.current_screen.ids.GL.add_widget(add)
        self.manager.current_screen.ids.GL.add_widget(total)

        for i in range(get_len(cat_dict['stayAt'])):
            label = Label(text=s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0], font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][1]), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            
            # Add widget.
            self.manager.current_screen.ids.GL.add_widget(clear)
            self.manager.current_screen.ids.GL.add_widget(reset)
            self.manager.current_screen.ids.GL.add_widget(label)
            self.manager.current_screen.ids.GL.add_widget(decrease)
            self.manager.current_screen.ids.GL.add_widget(amount)
            self.manager.current_screen.ids.GL.add_widget(add)
            self.manager.current_screen.ids.GL.add_widget(total)

            ref_dict["add "+str(i)]=weakref.ref(add)
            ref_dict["decrease "+str(i)]=weakref.ref(decrease)
            ref_dict["amt "+str(i)]=weakref.ref(amount)
            ref_dict["total "+str(i)]=weakref.ref(total)
            ref_dict["label "+str(i)]=weakref.ref(label)
            ref_dict["clear "+str(i)]=weakref.ref(clear)
            ref_dict["reset "+str(i)]=weakref.ref(reset)

            add.bind(on_press=self.manager.current_screen.adder)
            decrease.bind(on_press=self.manager.current_screen.decrease)
            clear.bind(on_press=self.manager.current_screen.remove)
            reset.bind(on_press=self.manager.current_screen.reset)

class CategoriesWindow(Screen):
    fmaterialsName = ObjectProperty(None)
    fmaterialsAmount = ObjectProperty(None)
    fmaterialsExpire = ObjectProperty(None)
    def on_kv_post(self, obj):
        pass

    def adder(self, instance):
        a = self.get_id(instance)

        # update amount on screen.
        amt = int(ref_dict["amt "+a]().text)+1
        ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(int(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1]) + int(amt))

    def decrease(self, instance):
        a = self.get_id(instance)
        
        # update amount on screen.
        if int(ref_dict["amt "+a]().text)>0:
            amt = int(ref_dict["amt "+a]().text)-1
            ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1] + int(ref_dict["amt "+a]().text))

    def remove(self, instance):
        a = self.get_id(instance)
        # loop remove widget.
        for id in ref_dict:
            if a in id:
                self.ids.GL.remove_widget(ref_dict[id]())

                # Move Index to replace old weakref\
                i = id.split()
                for j in range(int(i[-1]), get_len(cat_dict['stayAt'])-1):
                    ref_dict[i[0]+' '+str(j)] = ref_dict[i[0]+' '+str(j+1)]

        print(ref_dict.keys())
        # print(s.printCategory())
        name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][0]
        s.getCategory(cat_dict['stayAt']).removeType(name)
        # print(s.getCategory('Meat1').printType())

        n = math.ceil(get_len(cat_dict['stayAt']))+1
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n)

    def reset(self, instance):
        a = self.get_id(instance)
        
        ref_dict["amt "+a]().text = str(0)
        ref_dict["total "+a]().text = str(0)

    def get_id(self, instance):
        ref_instance = weakref.ref(instance)
        for id in ref_dict:
            if ref_instance == ref_dict[id]:
                return id.split()[-1]

    def back(self):
        print("Button on click: back")
        self.ids.GL.clear_widgets()
        ref_dict.clear()
        self.materialsName.text=""
        self.materialsAmount.text=""
        self.materialsExpire.text=""

    def adding_item(self):
        # print(self.materialsName.text,self.materialsAmount.text,self.materialsExpire.text)
        
        if(self.materialsName.text != '' and self.materialsExpire.text != ''):
            print(self.materialsName.text,self.materialsAmount.text,self.materialsExpire.text)
            if self.materialsAmount.text == '': 
                self.materialsAmount.text = '0'
            s.getCategory(cat_dict['stayAt']).addNewType(self.materialsName.text,int(self.materialsAmount.text) ,float(self.materialsExpire.text))

            label = Label(text=self.materialsName.text, font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = self.materialsAmount.text, font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)

            self.ids.GL.add_widget(clear)
            self.ids.GL.add_widget(reset)
            self.ids.GL.add_widget(label)
            self.ids.GL.add_widget(decrease)
            self.ids.GL.add_widget(amount)
            self.ids.GL.add_widget(add)
            self.ids.GL.add_widget(total)

            ref_dict["add "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(add)
            ref_dict["decrease "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(decrease)
            ref_dict["amt "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(amount)
            ref_dict["total "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(total)
            ref_dict["label "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(label)
            ref_dict["clear "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(clear)
            ref_dict["reset "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(reset)

            add.bind(on_press=self.adder)
            decrease.bind(on_press=self.decrease)
            clear.bind(on_press=self.remove)
            reset.bind(on_press=self.reset)

            n = math.ceil(get_len(cat_dict['stayAt']))+1
            self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n)

        self.materialsName.text=""
        self.materialsAmount.text=""
        self.materialsExpire.text=""
        
        # Add amount of Items
        for i in range(get_len(cat_dict['stayAt'])):
            item = ref_dict["label "+str(i)]().text
            amount = ref_dict["amt "+str(i)]().text
            total = ref_dict["total "+str(i)]().text
            print(item, amount, total)
            if int(total) == 0 and int(amount) == 0:
                name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0]
                print(name)
                s.getCategory(cat_dict['stayAt']).getType(name).clearItems()
            if int(amount)>0:
                name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0]
                s.getCategory(cat_dict['stayAt']).getType(name).addItem(int(amount))
            ref_dict["amt "+str(i)]().text = str(0)

        print("----------------------------------")
        print(s.getDisplayItem())
        
class UseWindow(Screen):
    def on_kv_post(self, obj):
        n = math.ceil(len(categories)/3)
        self.ids.SV.height = (40*(n-1)+190*(n))
        # loop create categories BTN.
        for i in range(len(categories)):
            button = Button(text=categories[i], font_name='fonts/THSarabun Bold.ttf', font_size = 36, size_hint_y = None, height = 190)
            button.bind(on_press=self.pressed)
            
            self.ids[categories[i]] = weakref.ref(button)
            self.ids.BL1.add_widget(button)

    def pressed(self, instance):
        print("Button on click:", instance.text)
        cat_dict['stayAt'] = instance.text
        # print(instance.text)
        self.manager.current = 'usecategories'
        self.manager.current_screen.ids.titleTXT.text = instance.text

        # generate widget.
        n = get_len(cat_dict['stayAt'])+1/1
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n) # กำหนดช่วงความสูงของ GridLayout ใน ScrollView
        
        label = Label(text='ชื่อวัตถุดิบ', font_size=24, size_hint_y=None, height=40,font_name='fonts/THSarabun Bold.ttf')
        amount = Label(text='จำนวน', font_size=24, size_hint_x=0.1, size_hint_y=None, height=40,font_name='fonts/THSarabun Bold.ttf')
        add = Label(text="", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        decrease = Label(text="", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        clear = Label(text=" ", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        reset = Label(text=" ", font_size=24, size_hint_y=None, height=40, size_hint_x=None, width=70,font_name='fonts/THSarabun Bold.ttf')
        total = Label(text = str('คงเหลือ'), font_size=24, size_hint_y=None, height=40, size_hint_x=0.1,font_name='fonts/THSarabun Bold.ttf')
                
        # Add widget.
        self.manager.current_screen.ids.GL.add_widget(clear)
        self.manager.current_screen.ids.GL.add_widget(reset)
        self.manager.current_screen.ids.GL.add_widget(label)
        self.manager.current_screen.ids.GL.add_widget(decrease)
        self.manager.current_screen.ids.GL.add_widget(amount)
        self.manager.current_screen.ids.GL.add_widget(add)
        self.manager.current_screen.ids.GL.add_widget(total)
        
        for i in range(get_len(cat_dict['stayAt'])):
            label = Label(text=s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0], font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][1]), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            
            # Add widget.
            self.manager.current_screen.ids.GL.add_widget(clear)
            self.manager.current_screen.ids.GL.add_widget(reset)
            self.manager.current_screen.ids.GL.add_widget(label)
            self.manager.current_screen.ids.GL.add_widget(decrease)
            self.manager.current_screen.ids.GL.add_widget(amount)
            self.manager.current_screen.ids.GL.add_widget(add)
            self.manager.current_screen.ids.GL.add_widget(total)

            ref_dict["add "+str(i)]=weakref.ref(add)
            ref_dict["decrease "+str(i)]=weakref.ref(decrease)
            ref_dict["amt "+str(i)]=weakref.ref(amount)
            ref_dict["total "+str(i)]=weakref.ref(total)
            ref_dict["label "+str(i)]=weakref.ref(label)
            ref_dict["clear "+str(i)]=weakref.ref(clear)
            ref_dict["reset "+str(i)]=weakref.ref(reset)

            add.bind(on_press=self.manager.current_screen.adder)
            decrease.bind(on_press=self.manager.current_screen.decrease)
            clear.bind(on_press=self.manager.current_screen.remove)
            reset.bind(on_press=self.manager.current_screen.reset)

    def back(self):
        print("Button on click: back main")
        self.manager.current = 'main'
        self.manager.current_screen.ids.showlists.clear_widgets()

        for i in categories:
            if s.getCategory(i).getDisplayItem() != None:
                for j in range(get_len(i)):
                    name = s.getCategory(i).getDisplayItem()[j][0]
                    s.getCategory(i).getType(name).updateRemainingExpHour()

        showlists = s.getDisplayItem()
        bubbleSort(showlists)
        showlists.insert(0,["ชื่อวัตถุดิบ","จำนวนคงเหลือ","เวลาคงเหลือ (ชั่วโมง)"])

        n = math.ceil(len(showlists))
        self.manager.current_screen.ids.showlists.height = (40*(n+1)+70*n)

        for i in range(len(showlists)):
            if showlists[i][2] != "เวลาคงเหลือ (ชั่วโมง)" and float("{:.4f}".format(float(showlists[i][2]))) <= 0:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])
                expire = Label(text=str('0.0000'), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf',color=[1,200,200,1])

            else:
                label = Label(text=str(showlists[i][0]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                amount = Label(text=str(showlists[i][1]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                if showlists[i][2] == "เวลาคงเหลือ (ชั่วโมง)" :
                    expire = Label(text=str(showlists[i][2]), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
                else:
                    expire = Label(text=str("{:.4f}".format(float(showlists[i][2]))), font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')

            self.manager.current_screen.ids.showlists.add_widget(label)
            self.manager.current_screen.ids.showlists.add_widget(amount)
            self.manager.current_screen.ids.showlists.add_widget(expire)

class UseCategoriesWindow(Screen):
    def on_kv_post(self, obj):
        pass

    def adder(self, instance):
        a = self.get_id(instance)

        # update amount on screen.
        if int(ref_dict["total "+a]().text)>0:
            amt = int(ref_dict["amt "+a]().text)+1
            ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(int(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1]) - int(ref_dict["amt "+a]().text))

    def decrease(self, instance):
        a = self.get_id(instance)
        
        # update amount on screen.
        if int(ref_dict["amt "+a]().text)>0:
            amt = int(ref_dict["amt "+a]().text)-1
            ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1] - int(ref_dict["amt "+a]().text))

    def remove(self, instance):
        a = self.get_id(instance)
        # loop remove widget.
        for id in ref_dict:
            if a in id:
                self.ids.GL.remove_widget(ref_dict[id]())

                # Move Index to replace old weakref\
                i = id.split()
                for j in range(int(i[-1]), get_len(cat_dict['stayAt'])-1):
                    ref_dict[i[0]+' '+str(j)] = ref_dict[i[0]+' '+str(j+1)]
        print(s.getDisplayItem())
        print(ref_dict.keys())
        # print(s.printCategory())
        name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][0]
        s.getCategory(cat_dict['stayAt']).removeType(name)
        # print(s.getCategory('Meat1').printType())

        n = math.ceil(get_len(cat_dict['stayAt']))+1
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n)
        print(s.getDisplayItem())

    def reset(self, instance):
        a = self.get_id(instance)
        
        ref_dict["amt "+a]().text = str(0)
        ref_dict["total "+a]().text = str(0)

    def get_id(self, instance):
        ref_instance = weakref.ref(instance)
        for id in ref_dict:
            if ref_instance == ref_dict[id]:
                return id.split()[-1]

    def back(self):
        print("Button on click: back")
        self.ids.GL.clear_widgets()
        ref_dict.clear()

    def using_item(self):
        # Add amount of Items
        for i in range(get_len(cat_dict['stayAt'])):
            item = ref_dict["label "+str(i)]().text
            amount = ref_dict["amt "+str(i)]().text
            total = ref_dict["total "+str(i)]().text
            print(item, amount, total)
            if int(total) == 0 and int(amount) == 0:
                name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0]
                s.getCategory(cat_dict['stayAt']).getType(name).clearItems()
            if int(amount)>0:
                name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0]
                s.getCategory(cat_dict['stayAt']).getType(name).useItem(int(amount))
            ref_dict["amt "+str(i)]().text = str(0)

        print("----------------------------------")
        print(s.getDisplayItem())

class WindowManager(ScreenManager):
    pass

KV = Builder.load_file("stock.kv")

class StockApp(App):
    def build(self):
        return KV

if __name__ == "__main__":
    StockApp().run()