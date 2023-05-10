from PIL import ImageTk, Image
import os
from tkinter import Canvas

class Note_page:

    def __init__(self, window, bpm, signature1, signature2, data):
        self.window = window
        self.window.pack(padx=0, pady=0)
        self.canvas = Canvas(self.window, bg="white", width=800, height=500)
        self.canvas.pack()
        self.loc = {
            'altY1': 82, 'altY2': 162, 'altY3': 243, 'altY4': 327, 'altY5': 413,
            'linesDist': 3, 'shiftNoteUp': -9, 'shiftNoteDown': 9, 'shiftAltDi': 1, 'shiftAltBec': 1, 'shiftAltBem': -3,
            'shiftPause1': 9, 'shiftPause2': 9, 'shiftPause4': 12, 'shiftPause8': 13, 'shiftPause16': 16,
            'shiftKey': 15, 'shiftSign1': 5, 'shiftSign2': 20, 'shiftSignLine': 12, 'shiftLegUp': -10, 'shiftLegDown': 10,
            'backgroundX': 400, 'backgroundY': 300
        }
        dir = os.path.dirname(os.path.realpath(__file__))
        dir = dir.replace('\\', '//')
        dir = dir.replace('pages', '')
        self.imgs = {
            'background': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NewPage.png').resize((800, 500), Image.LANCZOS)),
            'sKey': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Skey.png').resize((40, 40), Image.LANCZOS)),
            'bKey': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Bkey.png').resize((40, 40), Image.LANCZOS)),
            'altDi': ImageTk.PhotoImage(image=Image.open(dir + 'pics//AltDi.png').resize((10, 20), Image.LANCZOS)),
            'altBec': ImageTk.PhotoImage(image=Image.open(dir + 'pics//AltBec.png').resize((9, 18), Image.LANCZOS)),
            'altBem': ImageTk.PhotoImage(image=Image.open(dir + 'pics//AltBem.png').resize((10, 20), Image.LANCZOS)),
            'note1': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Note1.png').resize((10, 7), Image.LANCZOS)),
            'noteUp2': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteUp2.png').resize((10, 25), Image.LANCZOS)),
            'noteDown2': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteDown2.png').resize((10, 25), Image.LANCZOS)),
            'noteUp4': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteUp4.png').resize((10, 25), Image.LANCZOS)),
            'noteDown4': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteDown4.png').resize((10, 25), Image.LANCZOS)),
            'noteUp8': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteUp8.png').resize((18, 25), Image.LANCZOS)),
            'noteDown8': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteDown8.png').resize((18, 25), Image.LANCZOS)),
            'noteUp16': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteUp16.png').resize((18, 25), Image.LANCZOS)),
            'noteDown16': ImageTk.PhotoImage(image=Image.open(dir + 'pics//NoteDown16.png').resize((18, 25), Image.LANCZOS)),
            'addLine': ImageTk.PhotoImage(image=Image.open(dir + 'pics//AddLine.png').resize((15, 1), Image.LANCZOS)),
            'signLine': ImageTk.PhotoImage(image=Image.open(dir + 'pics//AddLine.png').resize((20, 2), Image.LANCZOS)),
            'pause1': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Pause1.png').resize((7, 5), Image.LANCZOS)),
            'pause2': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Pause2.png').resize((7, 5), Image.LANCZOS)),
            'pause4': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Pause4.png').resize((10, 15), Image.LANCZOS)),
            'pause8': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Pause8.png').resize((9, 15), Image.LANCZOS)),
            'pause16': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Pause16.png').resize((10, 20), Image.LANCZOS)),
            'tact': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Tact.png').resize((2, 23), Image.LANCZOS)),
            'legUpShort': ImageTk.PhotoImage(image=Image.open(dir + 'pics//LegUp.png').resize((25, 15), Image.LANCZOS)),
            'legDownShort': ImageTk.PhotoImage(image=Image.open(dir + 'pics//LegDown.png').resize((25, 15), Image.LANCZOS)),
            'legUpLong': ImageTk.PhotoImage(image=Image.open(dir + 'pics//LegUp.png').resize((35, 15), Image.LANCZOS)),
            'legDownLong': ImageTk.PhotoImage(image=Image.open(dir + 'pics//LegDown.png').resize((35, 15), Image.LANCZOS)),
            'num1': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num1.png').resize((22, 20), Image.LANCZOS)),
            'num2': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num2.png').resize((22, 20), Image.LANCZOS)),
            'num3': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num3.png').resize((22, 20), Image.LANCZOS)),
            'num4': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num4.png').resize((22, 20), Image.LANCZOS)),
            'num5': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num5.png').resize((22, 20), Image.LANCZOS)),
            'num6': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num6.png').resize((22, 20), Image.LANCZOS)),
            'num7': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num7.png').resize((22, 20), Image.LANCZOS)),
            'num8': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num8.png').resize((22, 20), Image.LANCZOS)),
            'num9': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num9.png').resize((22, 20), Image.LANCZOS)),
            'num10': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num10.png').resize((22, 20), Image.LANCZOS)),
            'num11': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num11.png').resize((22, 20), Image.LANCZOS)),
            'num12': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num12.png').resize((22, 20), Image.LANCZOS)),
            'num13': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num13.png').resize((22, 20), Image.LANCZOS)),
            'num14': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num14.png').resize((22, 20), Image.LANCZOS)),
            'num15': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num15.png').resize((22, 20), Image.LANCZOS)),
            'num16': ImageTk.PhotoImage(image=Image.open(dir + 'pics//Num16.png').resize((22, 20), Image.LANCZOS))
        }

        field_data = self.getFields(data)
        self.showNotes(signature1, signature2, data, 's', field_data[0], field_data[1])
        self.window.mainloop()


    def getFields(self, data):
        # FIND QUANTITY OF SYMBOLS FOR EACH TACT
        tact = 1
        currentQuant = 0
        quantOfSymb = []
        for i, note in data.iterrows():
            if note['tact'] == tact:
                if note['alternation'] != 'None':
                    currentQuant += 1
                currentQuant += 1
            else:
                quantOfSymb.append([tact, currentQuant])
                tact = note['tact']
                currentQuant = 1
        quantOfSymb.append([tact, currentQuant])
        lastTact = tact

        # FIND QUANTITY OF SYMBOLS FOR EACH FIELD
        fields = []
        symbQuant = 0
        tactQuant = 0
        cnt = 1
        for i in range(len(quantOfSymb)):
            if symbQuant + quantOfSymb[i][1] <= 40:
                tactQuant += 1
                symbQuant += quantOfSymb[i][1]
            else:
                fields.append([cnt, tactQuant, symbQuant])
                cnt += 1
                tactQuant = 1
                symbQuant = quantOfSymb[i][1]
        fields.append([cnt, tactQuant, symbQuant])

        return fields, lastTact


    def showNotes(self, signature1, signature2, data, key, fields, lastTact):
        background = self.imgs['background']
        self.canvas.create_image(self.loc['backgroundX'], self.loc['backgroundY'], image=background)
        # PRINT DATA
        theStart = 55
        theEnd = 755
        tact = 1
        for i in range(len(fields)):
            field = fields[i][0]
            if field == 1:
                tactQuant = fields[i][1]
            else:
                tactQuant = fields[i][1] + fields[i - 1][1]
            symbQuant = fields[i][2]
            if i < len(fields) - 1:
                # interval = (theEnd - theStart) / (symbQuant - 1)
                interval = (theEnd - (theStart + 55)) / (symbQuant - 1)
            else:
                # interval = 18
                interval = 17

            # PRINT S-KEY
            start = theStart
            start = self.printKey(field, start, key)
            start += 20
            start = self.printSignature(field, start, signature1, signature2)
            isLastTact = False

            # WHILE TACT IS ON FIELD
            while tact <= tactQuant:
                for k, note in data.iterrows():
                    # закрытие последнего такта
                    if k == len(data.index) - 1 and tact == lastTact:
                        start += (interval + 1) / 2
                        start = self.printTact(field, start)
                        start += 4
                        start = self.printTact(field, start)
                        tact += 1
                        break
                    if note['tact'] < tact:
                        continue
                    # закрытие обычного такта
                    if note['tact'] > tact:
                        tact += 1
                        start += (interval - 1) / 2
                        start = self.printTact(field, start)
                        start += (interval + 1) / 2
                        isLastTact = True
                        break
                    # нота
                    if note['octave'] != 0:
                        # не после тактовой черты
                        if not isLastTact:
                            start += interval
                        # печать
                        arr = self.printNote(field, start, key, int(note['octave']), int(note['note']), int(note['duration']), note['alternation'], interval)
                        start = arr[0]
                        line = arr[1]
                        tail = arr[2]

                        # с какой стороны легато
                        legDirection = 'Down'
                        if tail == 'Down':
                            legDirection = 'Up'
                        # длина легато (не используется)
                        length = 'Short'
                        if note['alternation'] != 'None':
                            length = 'Long'
                        # если есть легато
                        if note['leg'] == True:
                            amount = 1
                            start = self.printLeg(field, start, line, legDirection, length)
                        isLastTact = False
                    # пауза
                    else:
                        # не после такта
                        if not isLastTact:
                            start += interval
                        start = self.printPause(field, start, int(note['duration']))
                        isLastTact = False


    def printNote(self, fieldNum, xStart, key, octave, note, duration, alternation, interval):

        pointLocation = self.loc[f'altY{fieldNum}']
        shift_add_line_if_tail = 0

        # TAIL DIRECTION
        if key == 's':
            oct = octave
            if octave < 0:
                oct = octave + 1
            line = 12 + (1 - oct) * 7 - note

            if octave > 1 or (octave == 1 and note >= 7):
                tail = 'Down'
            else:
                tail = 'Up'
        elif key == 'b':
            oct = octave
            if octave < 0:
                oct = octave + 1
            line = (1 - oct) * 7 - note

            if octave > -1 or (octave == -1 and note >= 2):
                tail = 'Down'
            else:
                tail = 'Up'
        if duration == 1:
                tail = ''

        if tail == 'Up' and duration > 4:
            shift_add_line_if_tail = -5
        if tail == 'Down' and duration > 4:
            shift_add_line_if_tail = 5

        # NOTE SHIFT
        notePic = self.imgs[f'note{tail}{duration}']
        noteShift = 0
        if tail != '':
            noteShift = self.loc[f'shiftNote{tail}']

        # PRINT ALTERNATION
        if alternation == 'Di' or alternation == 'Bem' or alternation == 'Bec':
            altShift = self.loc[f'shiftAlt{alternation}']
            altPic = self.imgs[f'alt{alternation}']
            self.canvas.create_image(xStart, pointLocation + altShift + (line - 1) * self.loc['linesDist'], image=altPic)
            xStart += interval

        # PRINT NOTE
        self.canvas.create_image(xStart, pointLocation + noteShift + (line - 1) * self.loc['linesDist'], image=notePic)

        # PRINT ADDITIONAL LINES
        if line > 10:
            ln = 11
            while ln <= line:
                self.canvas.create_image(xStart + shift_add_line_if_tail, pointLocation + (ln - 1) * self.loc['linesDist'], image=self.imgs['addLine'])
                ln += 2
        elif line < 0:
            ln = -1
            while ln >= line:
                self.canvas.create_image(xStart + shift_add_line_if_tail, pointLocation + (ln - 1) * self.loc['linesDist'], image=self.imgs['addLine'])
                ln -= 2
        elif duration <= 2 and line % 2 == 1:
                self.canvas.create_image(xStart + shift_add_line_if_tail, pointLocation + (line - 1) * self.loc['linesDist'], image=self.imgs['addLine'])
        return [xStart, line, tail]


    def printLeg(self, fieldNum, xStart, line, dir, length):
        width = 25
        if length == "Long":
            width = 35
        xShift = width / 2
        pointLocation = self.loc[f'altY{fieldNum}']
        self.canvas.create_image(xStart + xShift, pointLocation + self.loc[f'shiftLeg{dir}'] + (line - 1) * self.loc['linesDist'], image=self.imgs[f'leg{dir}{length}'])
        return xStart


    def printPause(self, fieldNum, xStart, duration):
        pointLocation = self.loc[f'altY{fieldNum}']
        self.canvas.create_image(xStart, pointLocation + self.loc[f'shiftPause{duration}'], image=self.imgs[f'pause{duration}'])
        return xStart


    def printKey(self, fieldNum, xStart, key):
        pointLocation = self.loc[f'altY{fieldNum}']
        img = self.imgs[f'{key}Key']
        self.canvas.create_image(xStart, pointLocation + self.loc['shiftKey'], image=img)
        return xStart


    def printSignature(self, fieldNum, xStart, sign1, sign2):
        pointLocation = self.loc[f'altY{fieldNum}']
        img1 = self.imgs[f'num{sign1}']
        img2 = self.imgs[f'num{sign2}']
        imgLine = self.imgs['signLine']
        self.canvas.create_image(xStart, pointLocation + self.loc['shiftSign1'], image=img1)
        self.canvas.create_image(xStart, pointLocation + self.loc['shiftSign2'], image=img2)
        self.canvas.create_image(xStart, pointLocation + self.loc['shiftSignLine'], image=imgLine)
        return xStart


    def printTact(self, fieldNum, xStart):
        pointLocation = self.loc[f'altY{fieldNum}']
        self.canvas.create_image(xStart, pointLocation + 13, image=self.imgs['tact'])
        return xStart
