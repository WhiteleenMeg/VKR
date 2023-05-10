from pages.main_page import Main_page
import source

import PySimpleGUI as sg
import re
# from pydub import AudioSegment
import wave
from datetime import datetime


class Import_page(Main_page):
    def __init__(self, master=None):
        self.channels = source.sound_settings.get('channels')
        self.rate = source.sound_settings.get('rate')
        self.chunk = source.sound_settings.get('chunk')
        self.new_page = 1
        layout = [
            [self.empty_space()],
            self.menu(self.new_page),
            [self.empty_space()],
            [self.title('ИМПОРТ ФАЙЛА')],
            [self.empty_space()],
            [sg.Text('Файл'), sg.InputText(size=(90, 2)), sg.FileBrowse(file_types=(("wav", "*.wav"),), size=(13, 1))],
            [self.empty_space()],
            [sg.Text('Темп, bpm: ', size=(20, 1)), sg.InputText(size=(93, 2), default_text=f"{source.default.get('bpm')}")],
            [self.empty_space()],
            self.signature1_field(),
            [self.empty_space()],
            self.signature2_field(),
            [self.empty_space()],
            [sg.Text('Начало трека, сек: ', size=(20, 1)), sg.InputText(size=(93, 2), default_text='0')],
            [self.empty_space(2)],
            [sg.Button(button_text="Сгенерировать ноты", size=(50, 1)), sg.Button(button_text="Сохранить midi", size=(50, 1))]
        ]
        window = sg.Window('File Compare', layout=layout, size=(800, 500))
        damaged = False
        while True:
            event, values = window.read()
            self.navigation(event)
            if event == 'Сгенерировать ноты' or event == 'Сохранить midi':
                if self.can_import(values):
                    try:
                        with wave.open(self.filename) as mywav:
                            duration_seconds = mywav.getnframes() / mywav.getframerate()
                    except:
                        sg.Print('Error', f'File {self.filename} is damaged.')
                        damaged = True
                    # sound = AudioSegment.from_file(self.filename)
                    # duration_seconds = int((len(sound) / 1000.0))
                    if duration_seconds - 3 < self.start:
                        sg.Print('Error', f'Start time cant be over {duration_seconds - 3} seconds for this file.')
                    elif not damaged:
                        data = self.get_data_from_wav(self.start)
                        if event == 'Сгенерировать ноты':
                            self.notes_page = self.show_notes(data)
                            self.notes_page[1].quit()
                            self.notes_page[1].destroy()
                        if event == 'Сохранить midi':
                            midi_filename = (self.filename.replace('.wav', '_')) + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mid')
                            self.create_midi(data, filename_midi=midi_filename)
                            sg.Print(f'File successfully saved as {midi_filename}.')

            if self.new_page != 1:
                window.close()
                break


    def can_import(self, values):
        able_to_import = True
        self.bpm = values[1]
        self.filename = values[0]
        if self.filename:
            file = re.findall('.+:\/.+\.+.', self.filename)
            if not file and file is not None:
                sg.Print('Error', 'File path is not valid.')
                able_to_import = False
            try:
                self.bpm = int(values[1])
                self.signature1 = int(values[2])
                self.signature2 = int(values[3])
                self.start = int(values[4])
            except:
                sg.Print('Error:', 'Please enter numeric values.')
                able_to_import = False
            if not self.signature1 > 0 and self.signature1 < 17 and self.signature2 > 0 and self.signature2 < 17 and self.signature2 % 2 == 0:
                sg.Print('Error:', 'Values of signature must be in range [1, 16]. Signature denominator can only be equal to 2, 4, 8 or 16.')
                able_to_import = False
        else:
            sg.Print('Error', 'Please choose file.')
            able_to_import = False
        return able_to_import


