import kivy
import math
import weakref
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
Config.set('graphics', 'width', '1440')
Config.set('graphics', 'height', '1024')
# Config.set('graphics', 'resizable', False)

categories = ['เนื้อสัตว์','ผัก','อาหารทานเล่น','เครื่องดื่ม','ผลไม้','น้ำซุป','ของหวาน', 'น้ำจิ้ม','อื่นๆ', 'New']

Meat = ['Chicken', 'Pork', 'Beef', 'Fish']*100

class Materials:

    def __init__(self):
        self.name = ''
        self.amount = 0
        self.expire = 0.0

    def setName(self, name):
        self.name = name

    def setAmount (self, amount):
        self.amount = amount

    def setExpire(self, expire):
        self.expire = expire

class MainWindow(Screen):
    item = ObjectProperty(None)

    def Btn(self):
        print("Search: ",self.item.text)
    pass

class AddWindow(Screen):
    def on_kv_post(self, obj):
        n = math.ceil(len(categories)/3)
        self.ids.SV.height = (40*(n-1)+190*(n))
        for i in range(len(categories)):
            button = Button(text=categories[i], font_name='fonts/THSarabun Bold.ttf', font_size = 36, size_hint_y = None, height = 190)
            button.bind(on_press=self.pressed)
            self.ids[categories[i]] = weakref.ref(button)
            # with self.ids[categories[i]].canvas.before:
            #     Color(rgba=(0,0,0,0.3))
            #     RoundedRectangle(size=(1310/3, 190),pos=button.pos, radius = [(40, 40), (40, 40), (40, 40), (40, 40)])
            self.ids.BL1.add_widget(button)

    def pressed(self, instance):
        print("Button on click:", instance.text)
        # print(instance.text)
        self.manager.current = 'categories'
        self.manager.current_screen.ids.titleTXT.text = instance.text

class CategoriesWindow(Screen):
    def on_kv_post(self, obj):
        items = []
        with open('meat.txt') as reader:
            for line in reader.readlines():
                items.append(line)
        for i in range(len(items)):
            items[i] = items[i].split()
        n = math.ceil(len(items)/1)
        self.ids.GL.height = (40*(n+1)+50*n) # กำหนดช่วงความสูงของ GridLayout ใน ScrollView
        for i in range(len(items)):
            label = Label(text=items[i][0], font_size=24, size_hint_y=None, height=50)
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=50, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=50,size_hint_x=0.1)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=50, size_hint_x=0.1)
            clear = Button(text="C", font_name='fonts/THSarabun Bold.ttf', font_size=24, size_hint_y=None, height=50, size_hint_x=0.1)
            reset = Button(text="R", font_name='fonts/THSarabun Bold.ttf', font_size=24, size_hint_y=None, height=50, size_hint_x=0.1)
            total = Label(text = items[i][1], font_size=24, size_hint_y=None, height=50, size_hint_x=0.1)
            
            # Add widget.
            self.ids.GL.add_widget(clear)
            self.ids.GL.add_widget(reset)
            self.ids.GL.add_widget(label)
            self.ids.GL.add_widget(decrease)
            self.ids.GL.add_widget(amount)
            self.ids.GL.add_widget(add)
            self.ids.GL.add_widget(total)
    
    def adder(self, instance):
        pass



class WindowManager(ScreenManager):
    pass

KV = Builder.load_file("stock.kv")

class StockApp(App):
    def build(self):
        return KV

if __name__ == "__main__":
    StockApp().run()