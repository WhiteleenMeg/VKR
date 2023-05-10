from pages.main_page import Main_page
import source

import PySimpleGUI as sg
from threading import Thread, Event
import re


class Listen_page(Main_page):
    def __init__(self, master=None):
        self.new_page = 3
        layout = [
            [self.empty_space()],
            self.menu(self.new_page),
            [self.empty_space()],
            [self.title('ВОСПРОИЗВЕДЕНИЕ')],
            [self.empty_space()],
            [sg.Text('Файл'), sg.InputText(size=(90, 2)), sg.FileBrowse(file_types=(("mid", "*.mid"),), size=(13, 1))],
            [self.empty_space(2)],
            [sg.Button(button_text="Сгенерировать ноты (пока не готово)", size=(50, 1), disabled=True), sg.Button(button_text="Воспроизвести", size=(50, 1))]
        ]
        window = sg.Window('File Compare', layout=layout, size=(800, 500))
        while True:
            event, values = window.read()
            self.navigation(event)
            if event == 'Сгенерировать ноты':
                if self.can_import(values):
                    data = self.get_data_from_midi(self.start)
                    self.notes_page = self.show_notes(data)
                    self.notes_page[1].quit()
                    self.notes_page[1].destroy()
            if event == 'Воспроизвести':
                if self.can_import(values):
                    try:
                        self.play_midi()
                    except:
                        sg.Print('Error', 'Somethng is wrong with file.')

            if self.new_page != 3:
                window.close()
                break


    def can_import(self, values):
        able_to_import = True
        self.filename = values[0]
        if self.filename:
            file = re.findall('.+:\/.+\.+.', self.filename)
            if not file and file is not None:
                sg.Print('Error', 'File path is not valid.')
                able_to_import = False
        else:
            sg.Print('Error', 'Please choose file.')
            able_to_import = False
        return able_to_import
