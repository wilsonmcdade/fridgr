# main.py for fridge mounted label maker with gui
# @author Wilson McDade www.wmcda.de

# general imports
import datetime
import logging

# other dependencies
from brother_ql import BrotherQLRaster, create_label
from PIL import Image, ImageDraw, ImageFont

# kivy imports
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

# Kivy app
class fridgr(App):

    '''
        Kivy build functio to loads the kv file and makes the window look
            pretty
        Returns a widget structure.
    '''
    def build(self):
        root = Builder.load_file('fridgr.kv'

        Window.clearcolor = (.85,.85,.85,1)
        
        return root

    '''
        Brother-ql can only print images so we have to create an image with PIL
            in order to print a label. 
        @param message: food type for the label
        @param user: person printing
    '''
    def print(self,message,user):
        
        labelsize = (696,500)

        # Creates text for image to be printed
        font = ImageFont.truetype('fonts/Junicode-Regular.ttf', 48)
        im = Image.new('RGB',labelsize, 'white')
        d = ImageDraw.Draw(im)
        time = datetime.datetime.now()
        # Puts date on image
        d.text((5,5),time.strftime('%a, %b %d, %Y', anchor='lb', font=font)
        # Puts name on image
        d.text((labelsize[0]-5,5),user,anchor='rb',font=font)
        # Puts item name on image
        d.text((labelsize[0]/2,2*(labelsize[1]/3)),message,anchor='mb',font=font)

        qlr = BrotherQLRaster('QL-710')
        create_label(qlr,im,'62',red=False,threshold=70,cut=True,rotate=0)
