from datetime import datetime

from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen

from datasources.network import get_ip_address_string
from datasources.weather import get_weather_data
from datasources.calendar_data import get_events


class ScreenMain(LcarsScreen):
    def __init__(self, cal = None):
        LcarsScreen.__init__(self)
        self.cal = cal
    
    def setup(self, all_sprites):
        self.background = LcarsBackgroundImage("assets/lcars_screen_1.png")

        all_sprites.add(self.background, layer=0)

        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (15, 44), "LCARS 105"),
                        layer=1)
                        
        all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "HOME AUTOMATION", 2),
                        layer=1)
        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "LIGHTS"),
                        layer=1)
        all_sprites.add(LcarsBlockSmall(colours.ORANGE, (211, 16), "CAMERAS"),
                        layer=1)
        all_sprites.add(LcarsBlockLarge(colours.BEIGE, (249, 16), "ENERGY"),
                        layer=1)

        self.ip_address = LcarsText(colours.BLACK, (444, 520),
                                    get_ip_address_string())
        all_sprites.add(self.ip_address, layer=1)

        # info text
        all_sprites.add(LcarsText(colours.WHITE, (192, 174), "EVENT LOG:", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (244, 174), "2 ALARM ZONES TRIGGERED", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (286, 174), "14.3 kWh USED YESTERDAY", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (330, 174), "1.3 Tb DATA USED THIS MONTH", 1.5),
                        layer=3)
        self.info_text = all_sprites.get_sprites_from_layer(3)

        # date display
        self.stardate = LcarsText(colours.BLUE, (12, 380), "STAR DATE 2311.05 17:54:32", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # buttons
        all_sprites.add(LcarsButton(colours.RED_BROWN, (6, 662), "LOGOUT", self.logoutHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.BEIGE, (107, 127), "SENSORS", self.sensorsHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.PURPLE, (107, 262), "CALENDAR", self.calendarHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.PEACH, (107, 398), "WEATHER", self.weatherHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.PEACH, (108, 536), "HOME", self.homeHandler),
                        layer=4)

        # gadgets
        # self.trajectory = LcarsGifImage("assets/gadgets/fwscan.gif", (277, 556), 100)
        # all_sprites.add(self.trajectory, layer=1)

        self.dashboard = LcarsImage("assets/gadgets/dashboard.png", (187, 232))
        self.dashboard.visible = False
        all_sprites.add(self.dashboard, layer=2)

        self.weather_labels = []
        self.weather_datas = []
        for i in range(4):
            self.weather_labels.append([
                LcarsText(colours.PEACH, (200, 20 + 150*(i + 1)), "TIME: ", 1.5),
                LcarsText(colours.PEACH, (240, 20 + 150*(i + 1)), "STAT: ", 1.5),
                LcarsText(colours.PEACH, (280, 20 + 150*(i + 1)), "TEMP: ", 1.5),
                LcarsText(colours.PEACH, (320, 20 + 150*(i + 1)), "RAIN: ", 1.5)
            ])
            self.weather_datas.append([
                LcarsText(colours.PEACH, (200, 80 + 150*(i + 1)), "", 1.5),
                LcarsText(colours.PEACH, (240, 80 + 150*(i + 1)), "", 1.5),
                LcarsText(colours.PEACH, (280, 80 + 150*(i + 1)), "", 1.5),
                LcarsText(colours.PEACH, (320, 80 + 150*(i + 1)), "", 1.5)
            ])
            for comp in self.weather_labels[-1]:
                comp.visible = False
                all_sprites.add(comp, layer = 1)
            for comp in self.weather_datas[-1]:
                comp.visible = False
                all_sprites.add(comp, layer = 1)

        self.calendar_events = []
        for i in range(5):
            self.calendar_events.append(LcarsText(colours.PURPLE, (180 + 60*i, 170), "", 1.5))
            all_sprites.add(self.calendar_events[-1], layer = 1)

        #all_sprites.add(LcarsMoveToMouse(colours.WHITE), layer=1)
        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/panel/220.wav").play()

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)

    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.beep1.play()

        if event.type == pygame.MOUSEBUTTONUP:
            return False

    def hideInfoText(self):
        if self.info_text[0].visible:
            for sprite in self.info_text:
                sprite.visible = False

    def showInfoText(self):
        for sprite in self.info_text:
            sprite.visible = True

    def hideWeatherComps(self):
        for w in self.weather_labels:
            for comp in w:
                comp.visible = False
        for w in self.weather_datas:
            for comp in w:
                comp.visible = False
    
    def showWeatherComps(self):
        for w in self.weather_labels:
            for comp in w:
                comp.visible = True
        for w in self.weather_datas:
            for comp in w:
                comp.visible = True

    def hideEvents(self):
        for comp in self.calendar_events:
            comp.visible = False

    def showEvents(self):
        for comp in self.calendar_events:
            comp.visible = True

    def sensorsHandler(self, item, event, clock):
        self.hideInfoText()
        self.dashboard.visible = True
        self.hideWeatherComps()
        self.hideEvents()

    def calendarHandler(self, item, event, clock):
        self.hideInfoText()
        self.dashboard.visible = False
        self.hideWeatherComps()

        if self.cal:
            events = get_events(self.cal)
            for idx, event in enumerate(events):
                if idx < 4:
                    self.calendar_events[idx].setText(f"{event['name']}: {event['start']} - {event['end']}")
            self.showEvents()

    def weatherHandler(self, item, event, clock):
        self.hideInfoText()
        self.dashboard.visible = False
        self.hideEvents()

        weather = get_weather_data()[::2]
        for i in range(4):
            self.weather_datas[i][0].setText(weather[i]['time'].strftime("%H:%M"))
            self.weather_datas[i][1].setText(weather[i]['status'])
            self.weather_datas[i][2].setText(str(weather[i]['temperature']) + " °F")

            self.weather_datas[i][3].setText(str(weather[i]['rainfall']) + "in" if weather[i]['rainfall'] > 0 else "")
            self.weather_labels[i][3].setText("RAIN: " if weather[i]['rainfall'] > 0 else "")
        self.showWeatherComps()

    def homeHandler(self, item, event, clock):
        self.showInfoText()
        self.dashboard.visible = False
        self.hideWeatherComps()
        self.hideEvents()
        
    def logoutHandler(self, item, event, clock):
        from screens.authorize import ScreenAuthorize
        self.loadScreen(ScreenAuthorize())


