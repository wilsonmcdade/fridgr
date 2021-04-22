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
from kivy.uix.widget import Widget
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

class QuickLabel(Screen):
    pass

class MainWindow(Screen):
    pass

class PreviewImg(RelativeLayout):


    def __init__(self, **kwargs):
        super(PreviewImg,self).__init__(**kwargs)

        self.im = Image(pos_hint={'top':1,'right':1},source=\
            "../tmp/preview.jpg")

        self.add_widget(self.im)

        Clock.schedule_interval(self.update_img,.5)

    def update_img(self,*args):
        
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
        self.currscan = "076808005844"
        self.expiry = 0

        self.autoscan = 0

        self.showpreview = False
        self.autoscan = False

        self.gen_config()

        self.gen_screens()

        Clock.schedule_interval(lambda dt: self.update(),.5)

        return self.root

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
            'fontfile':'../fonts/Poppins-Regular.ttf'
            },
            'printer':{
            'model':'QL-710W',
            'label':'62',
            'backend':'linux_kernel',
            'src':'file:///dev/usb/lp0'
            }}

    '''
    gen screens
    '''
    def gen_screens(self):
    
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
        self.sm.add_widget(QuickLabel())
        self.root.add_widget(self.sm)

        self.sm.current = 'HomeScreen'

        self.sm.get_screen("HomeScreen").bind(on_leave=self.leave_screen)
        self.sm.get_screen("NewLabel").bind(on_leave=self.leave_screen)
        self.sm.get_screen("AutoScan").bind(on_leave=self.leave_screen)
        self.sm.get_screen("ItemLookup").bind(on_leave=self.leave_screen)
        self.sm.get_screen("QuickLabel").bind(on_leave=self.leave_screen)

    '''
    updates label texts
    '''
    def update(self):
            
        ids = self.sm.get_screen(self.sm.current).ids

        if self.sm.current == "NewLabel":
            
            self.lastusr = self.user
            self.lastexp = self.expiry

            self.user = ids.usrspinr.text
            self.expiry = ids.expspinr.text

            if self.lastusr != self.user or self.expiry != self.lastexp:

                filename = self.config['general']['tmp_folder']+"preview.jpg"
                gen_preview(self,self.get_printinfo(),filename)
    

        if self.sm.current == "AutoScan":

            self.lastusr = self.user
            self.lastexp = self.expiry

            self.user = ids.usrspinr.text
            self.expiry = ids.expspinr.text

            if self.lastusr != self.user or self.expiry != self.lastexp:

                filename = self.config['general']['tmp_folder']+"preview.jpg"
                gen_preview(self,self.get_printinfo(),filename)

            ids.previewimg.update_img()
            ids.scanbtn.text = self.isAutoScanning()

        if self.sm.current == "QuickLabel":

            self.user = ids.usrspinr.text
            self.expiry = ids.expspinr.text
            self.product_name = ids.prodspinr.text

            self.showpreview = True
            
            filename = self.config['general']['tmp_folder']+"preview.jpg"
            gen_preview(self,self.get_printinfo(),filename)

            ids.previewimg.update_img()

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

        elif button == "autoscan":
            self.autoscan = not self.autoscan

    '''
    shows preview popup
    '''
    def popup_preview(self):
        self.previewimg = PreviewImg()

        self.popupWindow = Popup(title="Preview Window",content=self.previewimg,\
            size_hint=(None,None),size=(400,400))

        self.popupWindow.bind(on_dismiss=self.popup_preview_dismiss)

        self.popupWindow.open()

    '''
    dismisses popup
    '''
    def popup_preview_dismiss(self, *args):
        self.showpreview = False;
        
    '''
    is autoscanning happening?
    '''
    def isAutoScanning(self):
        
        if self.autoscan == False:
            return "Auto\nScan"
        else:
            return "   Stop\nScanning"

    '''
    prereqs for leaving a screenmanager screen.
        sets variables to default value
    '''
    def leave_screen(self, *args):
        
        self.showpreview = False
        self.autoscan = False

    '''
    makes printinfo for printlabel function
    @return printinfo json object
    '''
    def get_printinfo(self):
        printinfo = {
            'expiry'    :self.expiry,
            'user'      :self.user,
            'prod_name' :self.product_name,
            'barcode'   :self.currscan
            }

        return printinfo

    '''
    scan function, opens input for scanning
    '''
    def scan(self):
        
        self.root.currscan = scan_fromhid() 


if __name__ == '__main__':
    Config.set('graphics','fullscreen','false')
    #Config.set('graphics','window_state','maximized')
    Config.write()
    fridgr().run()
