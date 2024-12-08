from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label

import time

from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', '0')

import main


class SButton(Button):

    def __init__(self, xy, **kwargs):
        super().__init__(**kwargs)
        self.xy = xy
        self.flag_bomb = 0


class MinesweeperApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opened_ceils1 = []
        self.game = main.Minesweeper()
        self.game.generate_bobms()
        self.size_x = self.game.size_x
        self.size_y = self.game.size_y
        self.opened_ceils = []
        self.flags_bombs = []
        self.first_press = True

        self.ceils = self.size_x * self.size_y - len(self.game.bobms)

        self.start_time = time.time()

    def regame(self):

        for ch in self.field_front.children:
            ch.text = ' '
            ch.background_color = [1, 1, 1, 1]
            ch.flag_bomb = 0

        self.opened_ceils = []
        self.opened_ceils1 = []
        self.flags_bombs = []
        self.first_press = True
        self.game.generate_bobms()

    def replay(self, but):
        self.regame()
        self.popup.dismiss()
        self.start_time = time.time()

    def _replay(self, but):
        self.regame()
        self.popuplose.dismiss()
        self.start_time = time.time()

    def win(self):
        box = BoxLayout(orientation='vertical')
        _time = time.time() - self.start_time
        struct = time.localtime(_time)

        time_bar = Label(text=f'Your time is \n {int(_time // 60 // 60)}:{time.strftime("%M:%S", struct)}')
        box.add_widget(time_bar)

        buttons = BoxLayout(size_hint=(1, 0.1), orientation="horizontal")
        button1 = Button(text='Ok', size_hint=(0.4, 1))
        button2 = Button(text='Replay', size_hint=(0.4, 1), on_press=self.replay)

        buttons.add_widget(button1)
        buttons.add_widget(button2)
        box.add_widget(buttons)
        self.popup = Popup(title="You win!", content=box, auto_dismiss=False, size_hint=(None, None), size=(400, 400))

        # bind the on_press event of the button to the dismiss function
        button1.bind(on_press=self.popup.dismiss)

        # open the popup
        self.popup.open()

    def lose(self):
        box = BoxLayout(orientation='vertical')
        _time = time.time() - self.start_time
        struct = time.localtime(_time)

        time_bar = Label(text=f'Your time is \n {time.strftime("%M:%S", struct)}')
        box.add_widget(time_bar)

        buttons = BoxLayout(size_hint=(1, 0.1), orientation="horizontal")

        button1 = Button(text='Ok', size_hint=(0.4, 1))
        button2 = Button(text='Replay', size_hint=(0.4, 1), on_press=self._replay)

        buttons.add_widget(button1)
        buttons.add_widget(button2)
        box.add_widget(buttons)

        self.popuplose = Popup(title="You lose", content=box, auto_dismiss=False, size_hint=(None, None),
                               size=(400, 400))

        button1.bind(on_press=self.popuplose.dismiss)

        self.popuplose.open()

    def show_number(self, x, y):

        if (x, y) in self.opened_ceils1:
            return None
        else:
            self.opened_ceils1.append((x, y))

        if x == self.game.size_x or y == self.game.size_y or x < 0 or y < 0:
            return None

        if self.game.n_field[x][y] < 0:
            self.lose()
            return True
        if self.game.n_field[x][y] == 0:

            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:

                    if not (i == 0 and j == 0):
                        self.show_number(x + i, y + j)

        for but in self.field_front.children:
            if but.xy == (x, y):
                if self.game.n_field[x][y] == 0:
                    but.text = ''
                    but.background_color = [0, 0, 0, 0]
                else:
                    but.text = str(self.game.n_field[x][y])
                    but.background_color = [0, 0, 1, 1]

                self.opened_ceils.append((x, y))
                break

        print(len(self.opened_ceils), self.ceils)
        if len(self.opened_ceils) == self.ceils:
            self.win()
            return

    def on_touch_(self, but, mouse):
        if but.collide_point(*mouse.pos):
            if mouse.button == 'middle':
                if but.text == " " or but.text == '':
                    return

                flag_bombs = []
                xi, yj = but.xy

                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:

                        if (xi + i, yj + j) not in self.flags_bombs:
                            continue

                        flag_bombs.append((xi + i, yj + j))
                if len(flag_bombs) != int(but.text):
                    return
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:

                        if (xi + i, yj + j) in flag_bombs:
                            continue

                        if self.show_number(xi + i, yj + j):
                            return

            if mouse.button == 'right':
                if but.text != ' ':
                    return

                if but.flag_bomb == 1:
                    self.flags_bombs.remove(but.xy)
                    but.background_color = [1, 1, 1, 1]
                    but.flag_bomb = 0
                elif but.flag_bomb == 0:
                    self.flags_bombs.append(but.xy)
                    but.background_color = [1, 0, 0, 1]
                    but.flag_bomb = 1
            elif mouse.button == 'left':
                if but.flag_bomb != 0:
                    return
                x, y = but.xy

                if self.first_press:
                    while self.game.n_field[x][y] != 0:
                        self.game.generate_bobms()
                    self.first_press = False

                self.show_number(x, y)

    def build(self):

        self.field_front = GridLayout(rows=self.size_x, cols=self.size_y)

        for i in range(self.size_y):
            for j in range(self.size_x):
                a = SButton(
                    xy=(i, j),
                    text=" ",
                    size=(100, 100),
                    on_touch_down=self.on_touch_
                )
                self.field_front.add_widget(a)
        return self.field_front


if __name__ == '__main__':
    MinesweeperApp().run()
