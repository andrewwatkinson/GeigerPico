from picographics import PicoGraphics, DISPLAY_LCD_240X240

def dict_to_string_for_display(data: dict):
    return "\n\n".join([f"{value} {unit}" for unit, value in data.items()])

class LCD:
    def __init__(self, settings: dict):
        self.settings = settings
        self.display = PicoGraphics(display=DISPLAY_LCD_240X240)
        self.clear()

    def clear(self):
        BLACK = self.display.create_pen(0, 0, 0)
        WHITE = self.display.create_pen(255, 255, 255)
        self.display.set_pen(BLACK)
        self.display.clear()
        self.display.set_clip(0, 0, 240, 240)
        self.display.set_pen(WHITE)
        self.display.set_font(self.settings["font"])
        self.display.set_thickness(self.settings["thickness"])


    def text(self,text,  x=0, y=0):
        self.clear()
        self.display.text(text, x, y, scale=self.settings["font_size"])
        self.update()

    def update(self):
        self.display.update()

    def display_data(self, data: dict):
        self.clear()
        # put the data vertically in the center of the screen
        x = 0
        y = 120 - (len(data) * 10)
        self.text(dict_to_string_for_display(data))
        self.update()

    def display_data_grid(self, data: dict):
        self.clear()

        # writes the reading as text in the white rectangle
        self.display.text("{}".format(data["cpm"]) + "C/M", 3, 3, 0, 3)
        # draw another box
        self.display.rectangle(1, 30, 100, 25)
        # writes the reading as text in the white rectangle
        self.display.text("{}".format(data["usv/h"]) + "uSv/h", 3, 20, 0, 3)
        self.update()
    