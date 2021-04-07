# main.py for fridge mounted label maker with gui
# @author Wilson McDade www.wmcda.de

# general imports
import datetime
import logging
import os

# import printing
from print_label import printlabel

# kivy imports
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.anchorlayout import AnchorLayout

# Kivy app
class fridgr(App):

    '''
    Kivy build functio to loads the kv file and makes the window look
        pretty
    Returns a widget structure.
    '''
    def build(self):
        Window.clearcolor = (.85,.85,.85,1)
        #Window.show_cursor = False

        root= Builder.load_file('fridgr.kv')
        return root

if __name__ == '__main__':
    Config.set('graphics','fullscreen','false')
    #Config.set('graphics','window_state','maximized')
    Config.write()
    fridgr().run()
