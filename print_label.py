# print_label.py 
# built to interface with brother ql label maker
# @author: Wilson McDade wmcda.de

# other dependencies
from PIL import Image, ImageDraw, ImageFont

# Printing imports
from brother_ql import BrotherQLRaster
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert

'''
Brother-ql can only print images so we have to create an image with PIL
    in order to print a label. 
@param message: food type for the label
@param user: person printing
'''
def printlabel(self,message,user):
	
    labelsize = (696,200)
    # Creates text for image to be printed
    font = ImageFont.truetype('fonts/OstrichSans-Heavy.otf', 48)
    bigfont = ImageFont.truetype('fonts/OstrichSans-Heavy.otf', 90)
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
