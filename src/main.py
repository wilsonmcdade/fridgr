# main.py for fridge mounted label maker with gui
# @author Wilson McDade wmcda.de

# general imports
import datetime
import logging
import os

# local imports
from print_label import printlabel, gen_preview, btn_printlabel
from scanner import scan_fromhid, scan_fromstdin

# kivy imports
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.popup import Popup


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

class PreviewWindow(RelativeLayout):


    def __init__(self, **kwargs):
        super(PreviewWindow,self).__init__(**kwargs)

        self.im = Image(pos_hint={'top':1,'right':1},source=\
            "../tmp/preview.jpg")

        self.add_widget(self.im)

    def update_preview(self):
        
        self.im.reload()

# Kivy app
class fridgr(App):

    '''
    Kivy build functio to loads the kv file and makes the window look
        pretty
    #returns window root
    '''
    def build(self):
        Window.clearcolor = (.85,.85,.85,1)

        self.user = "Goose"
        self.product_name = "Bagels, stale"
        self.barcode = "076808005844"
        self.expiry = 0

        self.autoscan = 0

        self.showpreview = False

        self.gen_config()

        self.root = BoxLayout()
        
        self.root.add_widget(Builder.load_file(self.config['general']['kv_folder']\
            +'left.kv'))

        smwindow = Builder.load_file(self.config['general']['kv_folder']+\
            'center.kv')

        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(HomeScreen())
        self.sm.add_widget(NewLabel())
        self.sm.add_widget(AutoScan())
        self.sm.add_widget(ItemLookup())
        self.root.add_widget(self.sm)

        self.sm.current = 'NewLabel'

        Clock.schedule_interval(lambda dt: self.update(),1)

        return self.root

    '''
    is this autoscanning?
    '''
    def isAutoScanning(self):
        
        if self.autoscan == False:
            return "Auto\nScan"
        else:
            return "   Stop\nScanning"

    '''
    updates label texts
    '''
    def update(self):

        if self.sm.current == "NewLabel":
            
            # ids of current screen
            ids=self.sm.get_screen(self.sm.current).ids

            self.user = ids.usrspinr.text
            self.expiry = ids.expspinr.text

            if self.showpreview:


                filename = self.config['general']['tmp_folder']+"preview.jpg"
                gen_preview(self,self.get_printinfo(),filename)
    
                #self.popup_preview()                

                self.show.update_preview()

        if self.sm.current == "AutoScan":
            
            ids = self.sm.get_screen(self.sm.current).ids

            filename = self.config['general']['tmp_folder']+"preview.jpg"
            gen_preview(self,self.get_printinfo(),filename)

            self.show.update_preview()
            ids.scanbtn.text = isAutoScanning();

            

    '''
    makes config
    '''
    def gen_config(self):
        
        self.config = {
            'general':{
            'api':"https://world.openfoodfacts.org/api/v0/product/{0}.json",
            'tmp_folder':'../tmp/',
            'kv_folder':'kv/'
            },
            'labels':{
            'labelsizex': 696,
            'labelsizey': 200,
            'fontfile':'../fonts/OstrichSans-Heavy.otf'
            },
            'printer':{
            'model':'QL-710W',
            'label':'62',
            'backend':'linux_kernel',
            'src':'file:///dev/usb/lp0'
            }}

    '''
    shows preview popup
    '''
    def popup_preview(self):
        self.show = PreviewWindow()

        self.popupWindow = Popup(title="Preview Window",content=self.show,\
            size_hint=(None,None),size=(400,400))

        self.popupWindow.bind(on_dismiss=self.popup_preview_dismiss)

        self.popupWindow.open()

    '''
    dismisses popup
    '''
    def popup_preview_dismiss(self, *args):
        self.showpreview = False;

        return False

    '''
    makes printinfo for printlabel function
    @return printinfo json object
    '''
    def get_printinfo(self):
        printinfo = {
            'expiry'    :self.expiry,
            'user'      :self.user,
            'prod_name' :self.product_name,
            'barcode'   :self.barcode
            }

        return printinfo

    '''
    btnprs interprets a buttonpress
    '''
    def btnprs(self, button):
        
        if button == "printlabel":
            btn_printlabel(self,self.get_printinfo())

        elif button == "preview":
            self.showpreview = True

            filename = self.config['general']['tmp_folder']+"preview.jpg"

            gen_preview(self,self.get_printinfo(),filename)

            self.popup_preview()   
    

    '''
    scan function, opens input for scanning
    '''
    def scan(self):
        
        self.root.barcode = scan_fromhid() 


if __name__ == '__main__':
    Config.set('graphics','fullscreen','false')
    #Config.set('graphics','window_state','maximized')
    Config.write()
    fridgr().run()