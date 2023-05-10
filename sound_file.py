import source

import pandas as pd
import numpy as np
import scipy.signal as signal
import scipy.fft as fft
from scipy.io import wavfile
from aubio import source, pitch, onset
# import scipy.io.wavfile as wav
# from scipy.signal import medfilt
# from pydub import AudioSegment



class Sound_file():
    def __init__(self, filename, bpm, signature1, signature2, chunk, rate):
        self.filename = filename
        self.bpm = bpm
        self.signature1 = signature1
        self.signature2 = signature2
        self.chunk = chunk
        self.rate = rate


    def read_pitch(self, k=55):

        s = source(self.filename, self.rate, self.chunk)
        rate = s.samplerate
        pitch_o = pitch("default", self.chunk, self.chunk, rate)
        pitch_o.set_unit("freq")
        total_frames = 0
        raw_data = pd.DataFrame(columns=['time', 'freq'])
        while True:
            samples, read = s()
            cur_pitch = pitch_o(samples)[0]
            raw_data.loc[len(raw_data.index)] = [total_frames / float(rate), cur_pitch]
            total_frames += read
            if read < self.chunk:
                break

        # # Загрузка аудиофайла
        # audio = AudioSegment.from_file(self.filename)
        #
        # # Разделение аудио на интервалы в 0.05 секунды
        # interval_duration = 0.02  # Длительность интервала в секундах
        # num_intervals = int(np.ceil(audio.duration_seconds / interval_duration))
        #
        # # Расчет громкости в децибелах для каждого интервала
        # loudness = []
        # for i in range(num_intervals):
        #     start_time = i * interval_duration * 1000  # Конвертация в миллисекунды
        #     end_time = start_time + interval_duration * 1000
        #     interval = audio[start_time:end_time]
        #     loudness_db = interval.dBFS
        #     loudness.append(loudness_db)
        #
        # # Создание DataFrame для хранения данных
        # loudness_data = pd.DataFrame({'time': np.arange(0, num_intervals) * interval_duration,
        #                          'loudness_db': loudness})

        return raw_data


    # PITCHES TO SPECIAL FORMAT
    def adapt_data(self, raw_data, startTime):
        notesX = pd.DataFrame(columns=['time', 'octave', 'note', 'alternation'])
        notes = pd.DataFrame(columns=['tact', 'octave', 'note', 'alternation', 'duration', 'leg'])

        # FREQ TABLE
        csvfile = 'system//notes.csv'
        freqTable = pd.read_csv(csvfile)

        # REMOVE MERTONOME
        lastFreq = 0
        rev = raw_data.reindex(index=raw_data.index[::-1])
        for j, raw_note in rev.iterrows():
            if (raw_note['freq'] < 130 or raw_note['freq']) > 1000 and raw_note['freq'] > 0:
                raw_note['freq'] = lastFreq
            lastFreq = raw_note['freq']
        raw_data = rev.reindex(index=rev.index[::-1])

        # NOTS MIN PARTS
        fractionMain = 60.0 / self.bpm
        fractionFull = fractionMain * self.signature2
        fractionMin = fractionFull / 16
        tactMinPart = (16.0 / self.signature2) * self.signature1
        arrFreq = np.array([])
        for j, raw_note in raw_data.iterrows():
            if raw_note['time'] < startTime:
                continue
            endTime = startTime + fractionMin
            if endTime < raw_note['time']:
                if np.mean(arrFreq) > 0:
                    freq = self.get_means(arrFreq)
                    lastRow = [0, 0, 'None', 0]
                    for k, freqRow in freqTable.iterrows():
                        if freqRow[3] < freq:
                            lastRow = freqRow
                            continue
                        # FIND CLOSER FREQ
                        if freq - lastRow[3] < freqRow[3] - freq:
                            notesX.loc[len(notesX.index)] = [startTime, lastRow[0], lastRow[1], lastRow[2]]
                        else:
                            notesX.loc[len(notesX.index)] = [startTime, freqRow[0], freqRow[1], freqRow[2]]
                        break
                        # lastRow = freqRow
                else:
                    notesX.loc[len(notesX.index)] = [startTime, 0, 0, 'None']
                startTime = endTime
                arrFreq = np.array([])
            else:
                arrFreq = np.append(arrFreq, raw_note['freq'])

        # NOTES COMPLETED
        counter = 0
        tactCounter = 0
        lastnote = [0, 0, 0, 'None']
        lastTactNum = 1
        tactNum = 1
        lastAdded = True
        for j, notePart in notesX.iterrows():

            # CHECK TACT
            tactCounter += 1
            if tactCounter > tactMinPart:
                tactNum += 1
                tactCounter = 1

            # IF TACT CHANGED
            tn = tactNum
            if tactNum != lastTactNum:
                tn = lastTactNum

            # SAME NOTE TYPE
            if notePart['octave'] == lastnote[1] and notePart['note'] == lastnote[2] and notePart['alternation'] == lastnote[3]:
                counter += 1
                lastAdded = False

                # CLOSE LAST TACT
                if tactCounter == 1 and tactNum > 1:
                    if counter > 8 and counter < 16:
                        notes.loc[len(notes.index)] = [tn, lastnote[1], lastnote[2], lastnote[3], 2, True]
                        counter -= 8
                    notes = self.addDuration(notes, counter - 1, tn, lastnote, True)
                    counter = 1
                    lastAdded = True

                # CLOSE FULL NOTE
                elif counter > 16:
                    notes.loc[len(notes.index)] = [tn, lastnote[1], lastnote[2], lastnote[3],  1, True]
                    counter = 1
                    lastAdded = True

            # NEW NOTE TYPE
            else:
                if counter > 8 and counter < 16:
                    notes.loc[len(notes.index)] = [tn, lastnote[1], lastnote[2], lastnote[3],  2, True]
                    counter -= 8
                notes = self.addDuration(notes, counter, tn, lastnote, False)
                lastAdded = True
                counter = 1
            lastnote = notePart
            lastTactNum = tactNum

        # SAVE LAST NOTE
        if not lastAdded:
            if counter > 8 and counter < 16:
                notes.loc[len(notes.index)] = [tn, lastnote[1], lastnote[2], lastnote[3],  2, True]
                counter -= 8
            notes = self.addDuration(notes, counter, tn, lastnote, False)

        # CHECK LAST TACT FRACTIONS
        durCount = 0
        for i, note in notes.iterrows():
            if note['tact'] == tactNum:
                durCount += 1.0 / note['duration']
        alph = 0.02
        perf = self.signature1 / self.signature2

        # IF FRACTION LOST
        if not durCount > perf - alph:
            dur = perf - durCount
            i = 1
            while i <= 16:
                while dur >= 1.0 / i - alph:
                    dur -= 1.0 / i
                    notes.loc[len(notes.index)] = [tn, 0, 0, 'None', i, False]
                i *= 2

        return notes, notesX


    # ADD STANDARD NOTE
    def addDuration(self, notes, counter, tactNum, lastnote, leg):
        if counter == 1 or counter == 2 or counter == 4 or counter == 8 or counter == 16:
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  16 / counter, leg]
        elif counter == 3:
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  8, True]
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  16, leg]
        elif counter == 5:
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  4, True]
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  16, leg]
        elif counter == 6:
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  4, True]
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  8, leg]
        elif counter == 7:
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  4, True]
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  8, True]
            notes.loc[len(notes.index)] = [tactNum, lastnote[1], lastnote[2], lastnote[3],  16, leg]
        return notes


    # FIND AVERAGE EXCEPT ZEROS
    def get_means(self, array):
        array[np.where(array == 0)] = np.nan
        mean = np.nanmean(array)
        return mean

