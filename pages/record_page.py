from pages.main_page import Main_page
import source
    
import PySimpleGUI as sg
from threading import Thread, Event
import re
import pyaudio
import wave
import time
from datetime import datetime


class Record_page(Main_page):
    def __init__(self, master=None):
        self.channels = source.sound_settings.get('channels')
        self.rate = source.sound_settings.get('rate')
        self.chunk = source.sound_settings.get('chunk')
        self.new_page = 2
        self.stop_threads = Event()
        self.thread_recording = None
        self.thread_metronome = None
        self.sound_data = []
        self.rec_btn = sg.Button(button_text="Начать запись", size=(100, 1))
        self.p = pyaudio.PyAudio()
        self.sample_format = pyaudio.paInt16
        self.beat = self.empty_space()
        self.metr_txt = self.empty_space(1, 15)
        state = 0
        self.btn_to_notes = sg.Button(button_text="Сгенерировать ноты", size=(50, 1), disabled=True)
        self.btn_to_midi = sg.Button(button_text="Сохранить midi", size=(50, 1), disabled=True)
        layout = [
            [self.empty_space()],
            self.menu(self.new_page),
            [self.empty_space()],
            [self.title('ЗАПИСЬ ЗВУКА'), self.empty_space(1, 5), self.metr_txt, self.beat],
            [self.empty_space()],
            [sg.Text('Файл'), sg.InputText(size=(90, 2)), sg.FileSaveAs(file_types=(("wav", "*.wav"),), size=(13, 1))],
            [self.empty_space()],
            [sg.Text('Темп, bpm: ', size=(18, 1)), sg.InputText(size=(93, 2), default_text=f"{source.default.get('bpm')}")],
            [self.empty_space()],
            self.signature1_field(),
            [self.empty_space()],
            self.signature2_field(),
            [self.empty_space()],
            [self.rec_btn],
            [self.empty_space()],
            [self.btn_to_notes, self.btn_to_midi]
        ]
        window = sg.Window('File Compare', layout=layout, size=(800, 500))
        while True:
            event, values = window.read()
            self.navigation(event)
            if event == 'Начать запись' and state == 0:
                if self.can_record(values):
                    self.record_sound()
                    state = 1
                    self.rec_btn.Update(text='Стоп')
                event = None
            if event == 'Начать запись' and state == 1:
                self.finishRecording()
                self.rec_btn.Update(text='Начать запись', disabled=True)
                self.btn_to_notes.Update(disabled=False)
                self.btn_to_midi.Update(disabled=False)

            if event == 'Сгенерировать ноты' or event == 'Сохранить midi':
                if self.can_record(values):
                    data = self.get_data_from_wav()
                    if event == 'Сгенерировать ноты':
                        self.notes_page = self.show_notes(data)
                        self.notes_page[1].quit()
                        self.notes_page[1].destroy()
                    if event == 'Сохранить midi':
                        midi_filename = (self.filename.replace('.wav', '_')) + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mid')
                        self.create_midi(data, filename_midi=midi_filename)
                        sg.Print(f'File successfully saved as {midi_filename}.')
            if self.new_page != 2:
                window.close()
                break


    def can_record(self, values):
        able_to_record = True
        self.filename = values[0]
        if self.filename:
            file = re.findall('.+:\/.+\.+.', self.filename)
            if not file and file is not None:
                sg.Print('Error', 'File path is not valid.')
                able_to_record = False
            try:
                self.bpm = int(values[1])
                self.signature1 = int(values[2])
                self.signature2 = int(values[3])
            except:
                sg.Print('Error:', 'Please enter numeric values of bpm and signature.')
                able_to_record = False
            if not self.signature1 > 0 and self.signature1 < 17 and self.signature2 > 0 and self.signature2 < 17 and self.signature2 % 2 == 0:
                sg.Print('Error:', 'Values of signature must be in range [1, 16]. Signature denominator can only be equal to 2, 4, 8 or 16.')
                able_to_record = False
        else:
            sg.Print('Error', 'Please choose file.')
            able_to_record = False
        return able_to_record


    def record_sound(self):
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=self.channels, rate=self.rate, frames_per_buffer=self.chunk,
                    input_device_index=1, input=True)
        self.stop_threads.clear()
        self.thread_recording = Thread(target=self.recording, daemon=False)
        self.thread_metronome = Thread(target=self.metronome, daemon=False)
        self.thread_recording.start()
        self.thread_metronome.start()


    def recording(self):
        while not self.stop_threads.is_set():
            data = self.stream.read(self.chunk)
            self.sound_data.append(data)


    def metronome(self):
        color = ['#243A61', '#FFFFFF']
        counter = 0
        self.metr_txt.Update('Метроном:', text_color=color[1], font=('Helvetica', 10, 'bold'))
        interval = 60.0/self.bpm
        beat_counter = 1
        saved_time = time.perf_counter()
        while not self.stop_threads.is_set():
            new_time = time.perf_counter()
            if new_time - saved_time > interval:
                if beat_counter == 1:
                    self.beat.Update(background_color=color[counter % 2], font=('Helvetica', 20, 'bold'))
                else:
                    self.beat.Update(background_color=color[counter % 2], font=('Helvetica', 7, 'bold'))
                if beat_counter == self.signature1:
                    beat_counter = 1
                else:
                    beat_counter += 1
                saved_time = new_time
                counter += 1


    def finishRecording(self):
        self.stop_threads.set()
        self.thread_recording = None
        self.thread_metronome = None
        self.stream.stop_stream()
        self.stream.close()

        self.p.terminate()
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.sound_data))
        wf.close()
