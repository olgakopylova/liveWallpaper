import json, sys, os, ctypes, time
from datetime import date, datetime
import calendar
#import Quartz
#from pynput import mouse
from PIL import Image, ImageDraw, ImageFont
import requests

class POINT(ctypes.Structure):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toString(self):
        return f'x: {self.x} y: {self.y}'



class File:
    def __init__(self, path):
        self.filename = f'resources/{path}'
        self.checkExist()
        self.content = False
        self.text = False

    def checkExist(self):
        if not os.path.exists(self.filename):
            self.createFile()
            self.save()

    def writeToFile(self, content):
        f = open(self.filename, 'w', encoding='utf8')
        f.write(content)
        f.close()

    def toString(self):
        return json.dumps(self.cache, indent=4, ensure_ascii=False)

    def save(self):
        self.writeToFile(self.toString())

    def readFile(self):
        f = open(self.filename, 'r', encoding='utf8')
        self.content = f.read()
        f.close()

    def read(self, i=0):
        if i > 1:
            print('Error read cache file.')
            sys.exit()
        self.readFile()
        try:
            self.text = json.loads(self.content)
        except:
            self.createFile()
            self.save()
            return self.read(i + 1)

    def createFile(self):
        self.text = {
            'version': 'v1.0'
        }


class Log(File):
    def __init__(self):
        path = f'resources/log/{Date.get("Y-m-d")}'
        File.__init__(self, path)

    def toString(self):
        return f'x: {self.x} y: {self.y}'

    def save(self):
        self.writeToFile(self.toString())

class Cache(File):
    def __init__(self):
        path = 'cache/settings.json'
        File.__init__(self, path)

    def toString(self):
        return json.dumps(self.text, indent=4, ensure_ascii=False)

    def save(self):
        self.writeToFile(self.toString())

    def put(self, index, body):
        self.text[index] = body
        self.save()

    def get(self, index, default):
        if index in self.text:
            return self.text[index]
        self.put(index, default)
        return default

cache = Cache()
cache.read()

class Date:
    def getDayName():
        now = date.today()
        # название дня на англ
        return calendar.day_name[now.weekday()]

    def get(*formats):
        date = datetime.now()
        if len(formats) == 1:
            return date.strftime(formats[0])
        back = []

        for i in formats:
            back.append(date.strftime(i))
        return tuple(back)

    def countDays():
        now = datetime.now()
        lastDay = datetime(day=15, month=7, year=2023)

        return (lastDay - now).days

class Color:
    def hex(s):
        n = int(s.lstrip('#'), 16)
        return (n >> 16, (n >> 8) & 0xff, n & 0xff)

class Cord:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x + w
        self.y2 = y + h

class Theme:
    def getList():
        return [ # todo сделать цвета от светлого к темному
            {'bg': Color.hex('#003b46'), 'fg': Color.hex('#c3dfe6'), 'text': Color.hex('#66a5ad')},
            {'bg': Color.hex('#131313'), 'fg': Color.hex('#980002'), 'text': Color.hex('#ffbf00')},
            {'bg': Color.hex('#ebdcb2'), 'fg': Color.hex('#af4425'), 'text': Color.hex('#552e1c')},
            {'bg': Color.hex('#1e0000'), 'fg': Color.hex('#bc6d4f'), 'text': Color.hex('#9d331f')},
            {'bg': Color.hex('#ddc5a2'), 'fg': Color.hex('#523634'), 'text': Color.hex('#b6452c')},
            {'bg': Color.hex('#ddc5a2'), 'fg': Color.hex('#523634'), 'text': Color.hex('#b6452c')},
            {'bg': Color.hex('#ddc5a2'), 'fg': Color.hex('#523634'), 'text': Color.hex('#b6452c')},
            {'bg': Color.hex('#ddc5a2'), 'fg': Color.hex('#523634'), 'text': Color.hex('#b6452c')},
            {'bg': Color.hex('#ddc5a2'), 'fg': Color.hex('#523634'), 'text': Color.hex('#b6452c')},
            {'bg': Color.hex('#ddc5a2'), 'fg': Color.hex('#523634'), 'text': Color.hex('#b6452c')},
            {'bg': Color.hex('#ddc5a2'), 'fg': Color.hex('#523634'), 'text': Color.hex('#b6452c')},
        ]

    def get():
        mode = (Date.countDays() // 30) - 1
        return Theme.getList()[mode]


def on_move(x, y):
    point = POINT(x, y)

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))

class OSManager:
    def __init__(self,):
        if sys.platform in ['linux', 'linux2']:
            self.os = LinOS()
        elif sys.platform in ['Windows', 'win32', 'cygwin']:
            self.os = WinOS()
        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            from appkit import NSWorkspace, NSColor, NSScreen, NSWorkspaceDesktopImageScalingKey, NSWorkspaceDesktopImageFillColorKey, NSImageScaleProportionallyUpOrDown
            from foundation import NSURL, NSDictionary
            self.os = MacOS()
        else:
            print("sys.platform={platform} is unknown. Please report."
                  .format(platform=sys.platform))
            print(sys.version)

    def getOS(self):
        return self.os

class Main:

    def __init__(self) -> object:
        self.osManager = OSManager()

        self.theme = Theme.get()

        self.width = int(self.osManager.os.getWeightScreen())
        self.height = int(self.osManager.os.getHeightScreen())

        self.render = Render(width=self.width, height=self.height, theme=self.theme)

        #self.mousePos = False
        #self.mouseDown = False

        self.openCities = False

    def setWallpaper(self, filename):
        self.render.setWallpaper(self.osManager.os, filename)

    def update(self):
        def cityBtn():
            self.openCities = True

        def setCity(index):
            Weather.setCity(index)
            self.openCities = False
            cache.put('weatherIndex', index)
            self.weather = Weather.getData()

        self.buttons = []
        self.render.generateEmpty()
        self.minutes, H_M, d_m_Y = Date.get('%M', '%H:%M', '%d.%m.%Y')

        theme = self.theme

        self.render.setFont('font.otf', 100)

        c = self.render.setCentralText(self.height / 3 - 100, Date.getDayName() + ' ' + d_m_Y)

        self.render.setFont('font.otf', 80)
        d = self.render.setCentralText(self.height / 3 - 10, str(Date.countDays()) + ' DAYS')

        self.render.setFont('font.otf', 45)

        if not self.openCities:
            self.render.setFont('font.otf', 40)
            if self.weather:
                self.render.setText(5, d.y2 + 20, f'{str(self.weather[1])}  {str(self.weather[2])}', theme['text'])

        try:
            self.render.save()
            self.setWallpaper('resources/tmp/wallpaper.png')
        except:
            print('smth went wrong')

    def start(self):
        while True:
            self.weather = Weather.getData()
            self.update()

            while self.minutes == Date.get('%M'):
                self.update()
                time.sleep(60)


class Weather:
    def getCities():
        return cache.get('weather', [
            ['Самара', 'https://www.gismeteo.ru/weather-samara-4618/'],
            ['Тольятти', 'https://www.gismeteo.ru/weather-tolyatti-4429/'],
            ['Москва', 'https://www.gismeteo.ru/weather-moscow-4368/']
        ])

    city = getCities()[cache.get('weatherIndex', 0)]

    def setCity(index):
        Weather.city = Weather.getCities()[index]

    def getJsonData():
        try:
            data = requests.get(Weather.city[1], headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}).text
            i = str.find(data, 'M.state.weather.cw = {')

            if i == -1:
                return False
            end = str.find(data[i:], '\n')

            if end == -1:
                return False

            return json.loads(data[i + 21: i + end])
        except:
            return False

    def getData():
        try:
            info = Weather.getJsonData()
            return (Weather.city[0], info['temperatureAir'][0], info['description'][0])
        except:
            return False


class Render:
    def __init__(self, width, height, theme):
        color = theme['bg']
        img = Image.new('RGB', (width, height), color)
        self.width, self.height = width, height

        self.orig = img
        img = self.orig.copy()

        self.object = img
        self.draw = ImageDraw.Draw(img)

        self.font = ImageFont.load_default()
        self.cashFonts = {}

        self.mousePos = False
        self.mouseDown = False

        self.idTheme = cache.get('themeIndex', 0)

        self.theme = Theme.get()

        self.font = ImageFont.load_default()
        self.cashFonts = {}

        self.bg = False
        self.bgLastColor = False

        self.openCities = False

        self.buttons = []

    def addButton(self, cord, function, update):
        self.buttons.append({'cord' : cord, 'function': function, 'update': update})

    def generateEmpty(self):
        if not self.bg or self.theme['bg'] != self.bgLastColor:
            color = self.theme['bg']
            img = Image.new('RGB', (self.width, self.height), color)

            self.original = img

        img = self.original.copy()

        self.object = img
        self.draw = ImageDraw.Draw(img)

    def getTextSize(self, text):
        new_box = self.draw.textbbox((0, 0), text, self.font)

        new_w = new_box[2] - new_box[0]  # bottom-top
        new_h = new_box[3] - new_box[1]  # right-left
        return new_w, new_h

    def setFont(self, name, size):
        id = f'{name}x{size}'
        if not id in self.cashFonts:
            self.cashFonts[id] = ImageFont.truetype(f'resources/fonts/{name}', size, encoding='UTF-8')
        self.font = self.cashFonts[id]

    def setText(self, x, y, text, color=(255, 255, 255)):
        self.draw.text((x, y), text, font=self.font, fill=color)
        w, h = self.getTextSize(text)
        return Cord(x, y, w, h)

    def setCentralText(self, y, text, color = (255, 255, 255)):
        x = self.width / 2
        w, h = self.getTextSize(text)
        return self.setText(int(x - w / 2), y, text, color)

    def save(self):
        self.object.save('resources/tmp/wallpaper.png')

    def setWallpaper(self, systemOS, filename):
        systemOS.setWallpaper(filename)

class OS:
    def setWallpaper(path):
        pass

    def getWeightScreen(self):
        pass

    def getHeightScreen(self):
        pass

    def toString(self):
        pass

class MacOS(OS):
    # todo отладить установку обоев только на один экран(основной)
    def setWallpaper(self, path):
        imageURL = NSURL.fileURLWithPath_(path)
        sharedSpace = NSWorkspace.sharedWorkspace()
        mainScreen = NSScreen.screens()[0]
        fillColor = NSColor.darkGrayColor()

        optDict = NSDictionary.dictionaryWithObjects_forKeys_([NSImageScaleProportionallyUpOrDown, fillColor],
                                                              [NSWorkspaceDesktopImageScalingKey,
                                                               NSWorkspaceDesktopImageFillColorKey])
        result, error = sharedSpace.setDesktopImageURL_forScreen_options_error_(imageURL, mainScreen, optDict, None)
        return result

    def getWeightScreen(self):
        return NSScreen.mainScreen().frame().size.width


    def getHeightScreen(self):
        return NSScreen.mainScreen().frame().size.height

    def toString(self):
        return 'MacOS'

class WinOS(OS):
    def setWallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, path, 2)
        return True

    def getHeightScreen(self):
        return ctypes.windll.user32.GetSystemMetrics(1)

    def getWeightScreen(self):
        return ctypes.windll.user32.GetSystemMetrics(0)

    def toString(self):
        return 'WinOS'

import Xlib.display
class LinOS(OS):
    def setWallpaper(self, path):
        command = "gsettings set org.gnome.desktop.background picture-uri file:/home/olga/PycharmProjects/liveWallpaper/" + path
        os.system(command)
        return True

    def getHeightScreen(self):
        resolution = Xlib.display.Display().screen().root.get_geometry()
        return resolution.height

    def getWeightScreen(self):
        resolution = Xlib.display.Display().screen().root.get_geometry()
        return resolution.width

    def toString(self):
        return 'LinOS'

if __name__ == "__main__":
   main = Main()
   main.start()
   #while True:
       #print(str(get_active_window()))
       #time.sleep(0.5)
    #with mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll) as listener:
    #    listener.join()