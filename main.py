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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

class HomeScreen(Screen):
    pass

class NewLabel(Screen):
    pass

class AutoScan(Screen):
    pass

class ItemLookup(Screen):
    pass

class MainWindow(Screen):
    pass


# Kivy app
class fridgr(App):

    '''
    Kivy build functio to loads the kv file and makes the window look
        pretty
    Returns a widget structure.
    '''
    def build(self):
        Window.clearcolor = (.85,.85,.85,1)
        # Window.show_cursor = False

        root = BoxLayout()
        
        root.add_widget(Builder.load_file('left.kv'))

        smwindow = Builder.load_file('fridgr.kv')

        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(HomeScreen())
        self.sm.add_widget(NewLabel())
        self.sm.add_widget(AutoScan())
        self.sm.add_widget(ItemLookup())
        root.add_widget(self.sm)

        self.sm.current = 'HomeScreen'

        root.add_widget(Builder.load_file('right.kv'))

        return root

    '''
    btnprs interprets a buttonpress
    '''
    def btnprs(self, button):
       pass 

if __name__ == '__main__':
    Config.set('graphics','fullscreen','false')
    #Config.set('graphics','window_state','maximized')
    Config.write()
    fridgr().run()
