# fridgr

![logo](https://user-images.githubusercontent.com/7411267/113955382-99e49280-97e9-11eb-87ff-f9ac326ab251.png)

Fridge Mounted Label-maker built with Python, Kivy, and Raspberry Pi

Read the blogpost at [wmcda.de/fridgr](https://www.wmcda.de/projects/fridgr)

## What is fridgr?

fridgr is a fridge mounted label maker and inventory system running on a Raspberry Pi. The program provides a GUI built in Python3 and Kivy, utilizes the [Open Food Facts](https://world.openfoodfacts.org/) live JSON API for UPC (barcode) lookup, and prints labels using the [Brother QL](https://github.com/pklaus/brother_ql) package to interface with a Brother QL 700 label printer.

## Usage

Fridgr is intended to be used in a household with a cavernous fridge in which the many household members forget items to expire, use items that aren't theirs, or a combination of the two. Fridgr seeks to provide a solution to this.  

Fridgr lets users quickly scan and print labels as they file items away in the fridge, optionally set expiry times and reminders, and even lookup the history of certain individual items in the local database.   

![stale bagels](https://user-images.githubusercontent.com/7411267/113955232-52f69d00-97e9-11eb-934e-c6929d11ee0c.png)

## Local Development / Implementation

Even though fridgr is built to run on a Raspberry Pi 3b+, with minor tweaks, the package can run on any machine capable of running Kivy and brother\_ql.

### Hardware Requirements

The original implementation of the fridgr system has the following build:

Item|Price
:---:|:---:
Raspberry Pi 3b+, 1 GB RAM, **Ethernet Connection**|$30-$40
[Raspberry Pi Touch Display](https://www.cytron.io/p-raspberry-pi-7-inch-touch-screen-display)|$73
Brother QL-710 Label Printer|$40-$100 Used, $400 New?
Handheld, Wired 2D Barcode Scanner|$20-$50
**Total**|~$160-$260

### Prerequisite Installation

At the moment I only have access to a Raspberry Pi 3b+ to run the system on. The installation instructions below are for installing the prerequisites on the Raspiberry Pi 3b+.

The packages being installed are mainly Kivy prerequisites. Install **Kivy 1.1.0** according to their installation instructions for your system and you should be set. Everything else is installed through pip, shown below.

#### Installing Kivy on a Raspberry Pi 3b+

This is a TL;DR of the Kivy docs [Installation on Raspberry Pi](https://kivy.org/doc/stable/installation/installation-rpi.html) page. Check there if you run into any issues.

This was my specific installation on a headless Raspberry Pi 3b+ running Raspberry Pi OS.

1.  Install dependencies
```
sudo apt update
sudo apt install pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   libgstreamer1.0-dev \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} libmtdev-dev \
   xclip xsel libjpeg-dev
```
2. Install more dependencies (SDL2 in my case)
```
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```
3. Update dynamic libraries
```
sudo ldconfig -v
```

**For Raspberry Pi Touch Display Only** 

4. Edit the file `~/kivy/config.ini` and add this to the [input] section 
```
mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
```

### Installing fridgr 

Installing fridgr and its dependencies

1. Clone the repo
```
git clone https://github.com/wilsonmcdade/fridgr
```
2. Create a virtual environment
```
python3 -m venv venv
```
3. Enter virtual environment
```
source venv/bin/activate
```
4. Install required files with pip
```
pip3 install -r requirements.txt
```
5. Run the app and enjoy 
```
python3 main.py
```
