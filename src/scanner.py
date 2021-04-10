# scanner.py for fridgr project
# Some code modified from https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100
# @author Wilson McDade wmcda.de

# General imports
import sys
import barcode
from barcode.writer import ImageWriter

hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 
        12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 
        19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 
        26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 
        33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 
        44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 
        52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 
        12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 
        19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 
        26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 
        33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 
        44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 
        52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

'''
scan_fromhid() function. opens scanner, receives input, and returns scanned input
@return Scanned input as string
'''
def scan_fromhid():

    fp = open('/dev/hidraw2', 'rb')

    shift = False
    eof = False
    buf = fp.read(8)

    code = ""

    while not eof:
        for c in buf:
            if c > 0:
                # Valid character

                char = int(ord(c))

                if char == 40:
                    eof = True
                    break;

                if shift:
                    
                    if char == 2:
                        shift = True

                    else:
                        ss += hid2[char]
                        shift = False

                else:
                    
                    if char == 2:
                        shift = True

                    else:
                        code += hid[char]

    return code

'''
scan_fromstdin() function. takes input as stdin (from keyboard), returns scanned input
@return scanned input as string
'''
def scan_fromstdin():

    barcode = input()

    return barcode

'''
generates barcode based from given input
@returns PIL image of barcode 
'''
def gen_barcode(code="076808005844"):
    EAN = barcode.get_barcode_class('ean13')
    ean=EAN(u"076808005844",writer=ImageWriter())
    ean.save('../tmp/barcode')

    return "../tmp/barcode.png"

'''
tests scanning functionality by printing scans to console
'''
def scan_test():

    fp = open('/dev/hidraw2', 'rb')

    shift = False
    eof = False
    buf = fp.read(8)

    code = ""

    while not eof:
        for c in buf:
            print(buf)
            print(c)
            if c > 0:
                # Valid character

                char = int(ord(c))

                if char == 40:
                    eof = True
                    break;

                if shift:
                    
                    if char == 2:
                        shift = True

                    else:
                        ss += hid2[char]
                        shift = False

                else:
                    
                    if char == 2:
                        shift = True

                    else:
                        code += hid[char]

        print(code)

