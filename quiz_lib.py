import os
import json
import IPython
import random
import pydub
from pydub import AudioSegment
import pyaudio
import wave
import ipywidgets as widgets
from IPython.display import Audio, display

item0 = widgets.Text(
        value='',
        placeholder='Type something',
        description='Mot:',
        disabled=False
    )

item1 = widgets.Text(
        value='',
        placeholder='Type something',
        description='Traduction:',
        disabled=False
    )

Record = widgets.Button(
        description='Record',
        disabled=False,
        button_style='',
        tooltip='Record',
        icon='fa-microphone',
    )
Record.path=""

description = widgets.Select(
        options=['nom commun', 'verbe', 'expression', 'phrase'],
        value='nom commun',
        description='type: ',
        disabled=False
    )

addToList = widgets.Button(
        description='Add to list',
        disabled=False,
        button_style='',
        tooltip='Click me',
        icon='plus'
    )

addToLib = widgets.Button(
        description='Add to library',
        disabled=False,
        button_style='',
        icon='plus'
    )

clear = widgets.Button(
    description='Clear existing Library'
)

output = widgets.Output()

vbox = widgets.VBox([item0, item1, Record, description, addToList, addToLib, output])

def recordAudioDescription(input):
    # Settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = input+".wav"
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def convertAudioDescription(input):
    wav_file = input+".wav"
    audio = AudioSegment.from_wav(wav_file)
    mp3_file = input+".mp3"
    audio.export(mp3_file, format="mp3")
    os.remove(wav_file)

    return mp3_file

def getAudioDescription(input):
    recordAudioDescription(input)
    path = convertAudioDescription(input)
    return path


def initLexique(count):
    lexique = [str(count)]
    return lexique

def isJson(jsonFilename):
    return os.path.exists(jsonFilename)

def createDictionnary(jsonFileName):
    library = dict()    
    if isJson(jsonFileName):
        with open(jsonFileName, 'r') as file:
            initialLib = json.load(file)
        library.update(initialLib) 
    else:
        with open(jsonFileName, 'w') as file:
            file.write('[]')
    cpt = 0
    lex = initLexique(cpt)
    
    def on_Record_click(b):
        with output:
            folderName = 'au-description/'
            inputName = folderName + item0.value
            getAudioDescription(inputName)
            Record.path = inputName+'.mp3'

    Record.on_click(on_Record_click)

    def on_addToList_click(b):
        with output:
            lex.append((item0.value, item1.value, Record.path, description.value))
            item0.value = ""
            item1.value = ""
            Record.path = ""
            print(f"{lex[-1][0]} <-> {lex[-1][1]} <- type = {lex[-1][3]}")

    addToList.on_click(on_addToList_click)

    def on_addToLib_click():
        library.update({lex[0]:lex[1:]})
        with open(jsonFileName, 'w') as file:
            json.dump(library,file)

    addToLib.on_click(on_addToLib_click())

    display(vbox)
    

def discoverMode(jsonFileName):
    with open(jsonFileName, 'r') as json_file:
        dico = json.load(json_file)
    if len(dico)<=1 :
        print("empty lexique")
        return 0
    index = random.randint(0, len(dico)-1)
    output = widgets.Output()
    FrenchWord = widgets.Button(
        description='',
        icon='question-circle'
    )
    def on_FrenchWord_click(b):
        with output:
            FrenchWord.description = dico[index][0]
            FrenchWord.icon = ''
    FrenchWord.on_click(on_FrenchWord_click)
    ArabicWord = widgets.Button(description=dico[index][1])
    if dico[index][2] != '':
        mp3_file = dico[index][2]
        audio_widget = Audio(mp3_file, autoplay=False)
        display(audio_widget)
    else :
        display(ArabicWord)
    display(FrenchWord)

    
