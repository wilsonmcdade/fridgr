# print_label.py 
# built to interface with brother ql label maker
# @author: Wilson McDade wmcda.de

# other dependencies
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import datetime

# Barcode imports
from scanner import gen_barcode

# Printing imports
from brother_ql import BrotherQLRaster
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert

'''
Gets preview of label, converts it to a jpg
'''
def gen_preview(self,printinfo,filename):
    pilimg = gen_pilimg(self,printinfo)

    pilimg.save(filename)

'''
Gets expiry and returns it as a date
'''
def get_expiry(expiry):
    dates = {
        '1 Day'     :    datetime.timedelta(days=1),
        '2 Days'    :   datetime.timedelta(days=2),
        '4 Days'    :   datetime.timedelta(days=4),
        '1 Week'    :   datetime.timedelta(weeks=1),
        '2 Weeks'   :  datetime.timedelta(weeks=2),
        '4 Weeks'   :  datetime.timedelta(weeks=4),
        'Never'     :    datetime.timedelta(weeks=52)
        }

    for key in dates:
        if expiry == key:
            return dates[key]

    return datetime.timedelta(days=2) 

'''
Generates a label as PIL with params and returns it
'''
def gen_pilimg(self,printinfo):
    cnfg = self.config['labels']

    labelsize = (cnfg['labelsizex'],cnfg['labelsizey'])

    fonts = {
        'tiny': ImageFont.truetype(cnfg['fontfile'],24),
        'norm': ImageFont.truetype(cnfg['fontfile'],48),
        'big': ImageFont.truetype(cnfg['fontfile'],90)
        }

    time = datetime.datetime.now()
    
    barcode_file = gen_barcode(printinfo)
    
    expiry = time+get_expiry(printinfo['expiry'])

    # Build image
    im = Image.new('RGB',(cnfg['labelsizex'],cnfg['labelsizey']+100),'white')
    d = ImageDraw.Draw(im)

    # date
    d.text((10,10),"Added:\t"+time.strftime('%a,%b,%d,%Y'), anchor='lt',fill='black',\
        font=fonts['tiny'])

    # user name
    d.text((labelsize[0]-10,10),printinfo['user'], anchor='rt',fill='black',\
        font=fonts['norm'])

    # expiry
    d.text((10,40),"Expires:\t"+expiry.strftime('%a,%b,%d,%Y'),anchor='lt',\
        fill='black',font=fonts['tiny'])

    # item name
    d.text((labelsize[0]/2,2*(labelsize[1]/3)),printinfo['prod_name'],\
        anchor='mm', fill='black', font=fonts['big'])

    barcode = Image.open(barcode_file)

    im.paste(barcode,((int)(cnfg['labelsizey']/2),(int)(cnfg['labelsizey']/1)))

    return im

'''
handles a print label button call
generated barcode, label
'''
def btn_printlabel(self,printinfo):
    
    printlabel(self,gen_pilimg(self,printinfo))

'''
Brother-ql can only print images so we have to create an image with PIL
    in order to print a label. 
@param message: food type for the label
@param user: person printing
'''
def printlabel(self,label):

    cnfg = self.config['printer']

    instructions = convert(
        qlr = BrotherQLRaster(cnfg['model']),
        images = [label],
        label = cnfg['label'],
        rotate = 0,
        threshold = 70.0,
        dither = False,
        compress = False,
        red = False,
        dpi_600 = False,
        no_cut = False)

    send(instructions,cnfg['src'],
        backend_identifier=cnfg['backend'],blocking=False)
