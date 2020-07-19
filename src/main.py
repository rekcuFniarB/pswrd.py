#!/usr/bin/env python3

##    Pswrd.py
##    Copyright (C) 2020  rekcuFniarB <retratserif@gmail.com>
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.



#import os
#os.environ['KIVY_TEXT'] = 'pil'

import kivy
kivy.require('1.11.1') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from lib import pswrd

class Pswrd(App):
    '''Main class'''
    def build(self):
        self.root  = ScreenManager()
        self.screens = {}
        self.screens['login'] = LoginScreen(name='login')
        self.root.add_widget(self.screens['login'])
        self.screens['main'] = MainScreen(name='main')
        self.root.add_widget(self.screens['main'])
        ## set active screen
        self.root.current = 'login'
        Window.bind(on_resize=self.on_resize_handler)
        return self.root

    def btn_exit(self, btn):
        ''' Return to login screen '''
        self.root.current = 'login'
    
    def get(self, btn):
        values = (
            self.screens['main'].type.btn_drop.text.lower().replace('none', ''),
            self.screens['login'].password.text,
            self.screens['main'].userName.text,
            self.screens['main'].domain.text,
            self.screens['main'].version.version.text,
        )
        result = pswrd.gen_from_list(
            values, alnum=self.screens['main'].version.alnum.active,
            compat=self.screens['main'].version.compat.active
        )
        _result = result
        if not self.screens['main'].result.show.active:
            result = pswrd.hide_part(result)
        self.screens['main'].result.result.text = result
        Clipboard.copy(_result)
    
    def on_resize_handler(self, obj, width, height):
        self.screens['main'].scroll.height = height - 45
        for screen in self.screens.values():
            if width < 400:
                screen.padding = ((width / 100) * 5, 0)
            else:
                screen.padding = ((width / 100) * 15, 0)

class LoginScreen(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        self.row_force_default = True
        self.row_default_height = 60
        self.padding = (70, 0)
        self.add_widget(Label(text='Master password:', size_hint=(1, None), height=60))
        self.password = TextInput(password=True, multiline=False, size_hint=(1, None), height=32)
        self.password.bind(on_text_validate=self.btn_open)
        self.add_widget(self.password)
        self.open = Button(text='Open', size_hint=(1, None), height=32)
        self.open.bind(on_press=self.btn_open)
        self.add_widget(self.open)
    
    def btn_open(self, btn):
        ''' "Open" button click handler. '''
        main.password = main.screens['login'].password.text
        main.root.current = 'main'
        
class MainScreen(GridLayout, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_x = 1
        self.padding = (70, 0)
        self.add_widget(Menu())
        self.scroll = ScrollView(size_hint=(1, None),
            size=(Window.width, Window.height-45)
        )
        grid = GridLayout(
            cols=1,
            size_hint=(1, None),
            height=500, # otherwise scrolling doesn't work
            row_force_default=True,
            row_default_height=50,
        )
        
        #grid.height=grid.minimum_height,
        grid.add_widget(Label(text='User Name (optional):', size_hint_y=None, height=30, center=(0, 0)))
        self.userName = TextInput(multiline=False, size_hint=(1,None), size=(300, 32),
            #pos_hint={'center_x': 100}, center=(0, 0)
        )
        grid.add_widget(self.userName)
        ## 2 columns row
        self.type = GridLayout(cols=2, height=32, width=300, size_hint=(1, None), center=(0, 0))
        self.type.add_widget(Label(text='Type:', height=32))
        self.type.drop = DropDown()
        self.type.types = ('None', 'Web', 'Email', 'Chat', 'Other')
        for t in self.type.types:
            _btn = Button(text=t, size_hint_y=None, height=32)
            _btn.bind(on_release=lambda _b: self.type.drop.select(_b.text))
            self.type.drop.add_widget(_btn)
        self.type.btn_drop = Button(text=self.type.types[0], size_hint=(None, None), height=32)
        self.type.btn_drop.bind(on_release=self.type.drop.open)
        self.type.drop.bind(on_select=lambda instance, x: setattr(self.type.btn_drop, 'text', x))
        self.type.add_widget(self.type.btn_drop)
        grid.add_widget(self.type)
        
        grid.add_widget(Label(text='Domain:'))
        self.domain = TextInput(multiline=False, size_hint_y=None, height=32)
        grid.add_widget(self.domain)
        
        ## 2 columns row
        self.version = obj2 = type('', (), {})
        _ = GridLayout(cols=2)
        _.add_widget(Label(text='Alnum:'))
        self.version.alnum = CheckBox()
        _.add_widget(self.version.alnum)
        grid.add_widget(_)
        _ = GridLayout(cols=2)
        _.add_widget(Label(text='Compat:'))
        self.version.compat = CheckBox()
        _.add_widget(self.version.compat)
        grid.add_widget(_)
        _ = GridLayout(cols=2)
        _.add_widget(Label(text='Version (default: 1)'))
        self.version.version = TextInput(multiline=False, text='1', size_hint=(None, None), width=32, height=32)
        _.add_widget(self.version.version)
        grid.add_widget(_)
        
        self.btn_get = Button(text='Get', on_press=main.get, size_hint_y=None, height=32)
        grid.add_widget(self.btn_get)
        self.result = GridLayout(cols=3, size_hint_y=None, height=40)
        self.result.result = TextInput(multiline=False, size_hint=(1, None), width=220, height=32)
        self.result.add_widget(self.result.result)
        self.result.show = CheckBox(size_hint=(None, None), width=32, height=32)
        self.result.show.bind(active=self.check_show)
        self.result.add_widget(self.result.show)
        self.result.add_widget(Label(text='Show', size_hint=(None, None), width=36, height=32))
        grid.add_widget(self.result)
        
        grid.bind(minimum_height=grid.setter('height'))
        self.scroll.add_widget(grid)
        self.add_widget(self.scroll)
        # Update scroll height on window resize
        #Window.bind(on_resize=self.on_resize_handler)
        
    def check_show(self, checkbox, value):
        main.get(self.btn_get)
    
class Menu(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.exit = Button(
            text='<',
            size_hint=(None, None),
            width=32, height=32,
            font_size=42, line_height=0,
            text_size=(32,22),
            #valign='top',
            halign='center',
        )
        self.exit.bind(on_press=main.btn_exit)
        self.add_widget(self.exit)

if __name__ == '__main__':
    main = Pswrd()
    main.run()
