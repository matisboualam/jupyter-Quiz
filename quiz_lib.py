import os
import json
import IPython
import random
import pydub
import pandas as pd
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

Description = widgets.Select(
        options=['nom commun', 'verbe', 'expression', 'phrase'],
        value='nom commun',
        description='type: ',
        disabled=False
    )

AddToList = widgets.Button(
        description='Add to list',
        disabled=False,
        button_style='',
        tooltip='Click me',
        icon='plus'
    )

Display = widgets.Button(
        description='Display',
        disabled=False,
        button_style='',
        tooltip='Click me',
        icon='plus'
    )

Clear = widgets.Button(
        description='Clear',
        disabled=False,
        button_style='',
        tooltip='Click me',
        icon='plus'
    )

output = widgets.Output()

vbox = widgets.VBox([item0, item1, Record, Description, AddToList, Display, Clear, output])

def recordAudioDescription(input):
    # Settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 2.5
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

def empty_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            empty_folder(file_path)

def createDictionnary(fileName):
    def on_Record_click(b):
        with output:
            folderName = 'au-description/'
            inputName = folderName + item0.value
            getAudioDescription(inputName)
            Record.path = inputName+'.mp3'

    Record.on_click(on_Record_click)

    def on_addToList_click(b):
        dictionnary = pd.read_csv(fileName)
        with output:
            data = {
                    'mot' : item0.value,
                    'trad' : item1.value, 
                    'lienAudio' : Record.path, 
                    'type' : Description.value
                    }
        dictionnary = pd.concat([dictionnary, pd.DataFrame([data])], ignore_index=True)
        print("Dictionnaire :\n", dictionnary)
        print("\n")
        dictionnary.to_csv('dictionnary.csv', index=False)

    AddToList.on_click(on_addToList_click)

    def on_display_click(b):
        dictionnary = pd.read_csv(fileName)
        print("Dictionnaire :\n", dictionnary)
        print("\n")

    Display.on_click(on_display_click)

    def on_clear_click(b):
        data = {'mot' : None,
                'trad' : None, 
                'lienAudio' : None, 
                'type' : None
                }
        pd.DataFrame([data]).to_csv('dictionnary.csv', index=False)
        empty_folder('au-description')

    Clear.on_click(on_clear_click)

    display(vbox)


    
