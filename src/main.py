#!/usr/bin/env python3

import kivy
kivy.require('1.11.1') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label

class Pswrd(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    Pswrd().run()
