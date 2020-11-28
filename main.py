# main.py for fridge mounted label maker with gui
# @author Wilson McDade www.wmcda.de

# general imports
import datetime
import logging
import os

# other dependencies
from PIL import Image, ImageDraw, ImageFont

# Brother_QL imports
from brother_ql import BrotherQLRaster
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert

# kivy imports
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder

# Kivy app
class fridgr(App):

	'''
	Kivy build functio to loads the kv file and makes the window look
	    pretty
	Returns a widget structure.
	'''
	def build(self):
		root = Builder.load_file('fridgr.kv')

		Window.clearcolor = (.85,.85,.85,1)
		Window.show_cursor = False

		return root

	'''
	Brother-ql can only print images so we have to create an image with PIL
	    in order to print a label. 
	@param message: food type for the label
	@param user: person printing
	'''
	def printlabel(self,message,user):
		
		labelsize = (696,200)

		# Creates text for image to be printed
		font = ImageFont.truetype('fonts/Junicode-Regular.ttf', 48)
		bigfont = ImageFont.truetype('fonts/Junicode-Regular.ttf', 90)
		im = Image.new('RGB',labelsize, 'white')
		d = ImageDraw.Draw(im)
		time = datetime.datetime.now()
		# Puts date on image
		d.text((10,10),time.strftime('%a, %b %d, %Y'), anchor='lt',
			fill='black', font=font)
		# Puts name on image
		d.text((labelsize[0]-10,10),user,anchor='rt', fill='black',
			font=font)
		# Puts item name on image
		d.text((labelsize[0]/2,2*(labelsize[1]/3)),message,anchor='mm',
			fill='black', font=bigfont)

		instructions = convert(
			qlr = BrotherQLRaster('QL-710W'),
			images = [im],
			label = '62',
			rotate = 0,
			threshold = 70.0,
			dither = False,
			compress = False,
			red = False,
			dpi_600 = False,
			no_cut = False)

		send(instructions,'file:///dev/usb/lp0',
			backend_identifier='linux_kernel',blocking=False)

if __name__ == '__main__':
	Config.set('graphics','fullscreen','auto')
	Config.set('graphics','window_state','maximized')
	Config.write()

	fridgr().run()
