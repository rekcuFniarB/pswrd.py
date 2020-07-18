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
from lib import pswrd

class Pswrd(App):
    '''Main class'''
    def build(self):
        self.root  = ScreenManager()
        self.loginScreen = LoginScreen(name='login')
        self.root.add_widget(self.loginScreen)
        self.mainScreen = MainScreen(name='main')
        self.root.add_widget(self.mainScreen)
        ## set active screen
        self.root.current = 'login'
        #self.clipboard = Clipboard()
        return self.root

    def btn_exit(self, btn):
        ''' Return to login screen '''
        self.root.current = 'login'
    
    def get(self, btn):
        values = (
            self.mainScreen.type.btn_drop.text.lower().replace('none', ''),
            self.loginScreen.password.text,
            self.mainScreen.userName.text,
            self.mainScreen.domain.text,
            self.mainScreen.version.version.text,
        )
        result = pswrd.gen_from_list(values, alnum=self.mainScreen.version.alnum.active, compat=self.mainScreen.version.compat.active)
        _result = result
        if not self.mainScreen.result.show.active:
            result = pswrd.hide_part(result)
        self.mainScreen.result.result.text = result
        Clipboard.copy(_result)

class LoginScreen(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        #self.add_widget(Label(text='User Name'))
        #self.username = TextInput(multiline=False)
        #self.add_widget(self.username)
        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False, size_hint_y=None, height=32, width=100)
        self.add_widget(self.password)
        self.open = Button(text='Open')
        self.open.bind(on_press=self.btn_open)
        self.add_widget(self.open)
    
    def btn_open(self, btn):
        ''' "Open" button click handler. '''
        main.password = main.loginScreen.password.text
        main.root.current = 'main'
        print(main.password)

class MainScreen(GridLayout, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Menu())
        self.add_widget(Label(text='User Name (optional)'))
        self.userName = TextInput(multiline=False, height=32)
        self.add_widget(self.userName)
        
        ## 2 columns row
        self.type = GridLayout(cols=2, height=32)
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
        self.add_widget(self.type)
        
        self.add_widget(Label(text='Domain'))
        self.domain = TextInput(multiline=False, height=32)
        self.add_widget(self.domain)
        
        ## 2 columns row
        self.version = GridLayout(cols=2)
        self.version.add_widget(Label(text='Alnum:'))
        self.version.alnum = CheckBox()
        self.version.add_widget(self.version.alnum)
        self.version.add_widget(Label(text='Compat:'))
        self.version.compat = CheckBox()
        self.version.add_widget(self.version.compat)
        self.version.add_widget(Label(text='Version (default: 1)'))
        self.version.version = TextInput(multiline=False, text='1', width=32, height=32)
        self.version.add_widget(self.version.version)
        self.add_widget(self.version)
        
        self.btn_get = Button(text='Get', on_press=main.get)
        self.add_widget(self.btn_get)
        self.result = GridLayout(cols=3)
        self.result.result = TextInput(multiline=False, height=32)
        self.result.add_widget(self.result.result)
        self.result.show = CheckBox(size_hint=(None, None))
        self.result.show.bind(active=self.check_show)
        self.result.add_widget(self.result.show)
        self.result.add_widget(Label(text='Show', size_hint=(None, None)))
        self.add_widget(self.result)
        
    def check_show(self, checkbox, value):
        main.get(self.btn_get)

class Menu(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.exit = Button(text='<')
        self.exit.bind(on_press=main.btn_exit)
        self.add_widget(self.exit)

if __name__ == '__main__':
    main = Pswrd()
    main.run()
