import source
from sound_file import Sound_file
from pages.note_page import Note_page

import PySimpleGUI as sg
from tkinter import *
import pygame
from mido import MidiFile, MidiTrack, MetaMessage, Message


class Main_page():

    def __init__(self, master=None):
        self.bpm = source.default.get('bpm')
        self.signature1 = source.default.get('signature1')
        self.signature2 = source.default.get('signature2')
        self.start = 0
        self.filename = ''
        
    def menu(self, num):
        return [sg.Button(button_text="Импорт wav", size=(22, 2), disabled=(num == 1)), sg.Button(button_text="Запись wav", size=(22, 2), disabled=(num == 2)), sg.Button(button_text="Воспроизведение midi", size=(22, 2), disabled=(num == 3)), sg.Button(button_text="Справка", size=(22, 2), disabled=(num == 4))]
   
   
    def title(self, text):
        return sg.Text(text, font=('Helvetica', 20, 'bold'), text_color='#243A61')


    def empty_space(self, size_vertical=1, size_horizontal=1):
        return sg.Text('', background_color=None, pad=(0,0), size=(size_horizontal, size_vertical))
    
    
    def navigation(self, event):
        if event == None:
            self.new_page = 0
        if event == 'Импорт wav':
            self.new_page = 1
        if event == 'Запись wav':
            self.new_page = 2
        if event == 'Воспроизведение midi':
            self.new_page = 3
        if event == 'Справка':
            self.new_page = 4


    def signature1_field(self):
        return [sg.Text('Числитель размера: ', size=(20, 1)), sg.Combo(['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'], size=(93, 2), default_value=f"{source.default.get('signature1')}")]

    
    def signature2_field(self):
        return [sg.Text('Знаменатель размера: ', size=(20, 1)), sg.Combo(['2','4','8','16'], size=(93, 2), default_value=f"{source.default.get('signature2')}")],


    def get_data_from_wav(self, start_time=0):
        sound_file = Sound_file(filename=self.filename, chunk=self.chunk, rate=self.rate, bpm=self.bpm, signature1=self.signature1, signature2=self.signature2)
        raw_data = sound_file.read_pitch()
        return sound_file.adapt_data(raw_data, start_time)


    def show_notes(self, data):
        page_num = 1
        root = Toplevel()
        snotes_window = Frame(root, width=800, height=500)
        return Note_page(snotes_window, 80, 4, 4, data[0]), root


    def create_midi(self, data_arr, filename_midi):
        data = data_arr[0]
        mid = MidiFile(type=0)
        track = MidiTrack()
        track.append(Message('program_change', program=1, time=0))
        track.append(MetaMessage('set_tempo', tempo=int((6*(10**7))/self.bpm), time=0))
        data_prev_note = ''
        delta_time = 0
        dur_time = 0
        k = self.signature2
        first_note = True
        long_note = False
        for i, data_note in data.iterrows():
            if not first_note:
                if data_prev_note['note'] != 0:
                    dur_time += 480 / data_note['duration'] * k
                    if not (data_note['note'] == data_prev_note['note'] and data_note['octave'] == data_prev_note['octave'] and data_note['alternation'] == data_prev_note['alternation']):
                        # закрытие ноты
                        prev_note = source.notes_midi.get(f"{data_prev_note['octave']} {data_prev_note['note']} {data_prev_note['alternation']}")
                        track.append(Message('note_off', note=int(prev_note), velocity=64, time=int(dur_time)))
                        long_note = False
                    else:
                        long_note = True
            # пауза начинается
            if data_note['note'] == 0:
                # разрыв между нотами увеличивается
                delta_time += 480 / data_note['duration'] * k
            # нота начинается
            elif not long_note:
                note = source.notes_midi.get(f"{data_note['octave']} {data_note['note']} {data_note['alternation']}")
                track.append(Message('note_on', note=int(note), velocity=64, time=int(delta_time)))
                # разрыв между нотами будет 0
                delta_time = 0
                # длина ноты пока 0
                dur_time = 0
            first_note = False
            data_prev_note = data_note

        if data_prev_note['note'] != 0:
            dur_time += 480 / data_prev_note['duration'] * k
            prev_note = source.notes_midi.get(f"{data_prev_note['octave']} {data_prev_note['note']} {data_prev_note['alternation']}")
            track.append(Message('note_off', note=int(prev_note), velocity=64, time=int(dur_time)))

        mid.tracks.append(track)
        mid.save(filename_midi)


    def play_midi(self):
        clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
