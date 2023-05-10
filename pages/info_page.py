from pages.main_page import Main_page
import source

import PySimpleGUI as sg
from threading import Thread, Event
import re


class Info_page(Main_page):
    def __init__(self, master=None):
        self.new_page = 4
        layout = [
            [self.empty_space()],
            self.menu(self.new_page),
            [self.empty_space()],
            [self.title('СПРАВКА')],
            [self.empty_space()],
            [sg.Text('Тут будет инфа о программе...')]
        ]
        window = sg.Window('File Compare', layout=layout, size=(800, 500))
        while True:
            event, values = window.read()
            self.navigation(event)
            if self.new_page != 4:
                window.close()
                break
