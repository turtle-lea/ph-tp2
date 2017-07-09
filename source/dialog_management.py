#!/usr/bin/env python
# coding=utf-8
import pyaudio
import wave
import sys
import requests
import json
import time
from requests.auth import HTTPBasicAuth
from pydub import AudioSegment
from TTS_and_STT import text_to_speech

username = "c2bd3588-ad8d-4405-a1c8-28ffde7beaee"
password = "wNINKHokHL1w"
speech_to_text_base = "https://stream.watsonplatform.net/speech-to-text/api/v1"
COMANDO_INVALIDO = "COMANDO_INVALIDO"

# VELOCIDAD. Estados: NORMAL, AUMENTADA
VELOCIDAD = "NORMAL"

# ORDEN. Estados: NORMAL, INVERTIDO
ORDEN = "NORMAL"

# REMOVER_PARTE. Estados: NINGUNA, INICIAL, MEDIA, FINAL
REMOVER_PARTE = "NINGUNA"
audios_folder = '../audios/'

"""PyAudio Example: Play a wave file."""
def play(audio_filename="audio.wav"):
    CHUNK = 1024

    wf = wave.open(audio_filename, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()

def reverse(orden):
    if orden == 'NORMAL':
        return
    audio = AudioSegment.from_wav("audio.wav")
    audio.reverse().export("audio.wav", format="wav")
    return

def speedup(velocidad):
    if velocidad == 'NORMAL':
        return
    audio = AudioSegment.from_wav("audio.wav")
    audio.speedup().export("audio.wav", format="wav")
    return

def remover_parte(remover_parte):
    global audios_folder
    if remover_parte == 'NORMAL':
        return
    audio = AudioSegment.from_wav("audio.wav")
    three_seconds = 3*1000
    audio_muy_corto = audios_folder + 'audio_muy_corto.wav'
    if audio.duration_seconds < 5 and remover_parte != "NINGUNA":
        play(audio_muy_corto)
        return
    if remover_parte == 'INICIAL':
        end = audio[-three_seconds:]
        end.fade_in(1500).export("audio.wav", format="wav")
        return

    if remover_parte == 'FINAL':
        beginning = audio[:three_seconds]
        beginning.fade_out(1500).export("audio.wav", format="wav")
        return

    if remover_parte == 'MEDIA':
        beginning = audio[:2*1000]
        end = audio[-2*1000:]
        beginning.append(end, crossfade=1000).export("audio.wav", format="wav")
        return

def comandos_seleccionados():
    global VELOCIDAD, ORDEN, REMOVER_PARTE
    text = " Por supuesto. Velocidad: " + VELOCIDAD + ". Orden: " + ORDEN + ". Remover parte: " + REMOVER_PARTE
    text_to_speech("comandos_seleccionados.wav", text, rate_change="+0%", f0mean_change="+0%")
    play("comandos_seleccionados.wav")

def manage():
    global VELOCIDAD, ORDEN, REMOVER_PARTE, COMANDO_INVALIDO
    message = asr('audio.wav')
    print message

    if ('aplicar' in message) or ('comando' in message):

        if ('modificar' in message) or ('orden' in message):
            if ('normal' in message) or ('cero' in message):
                cambiar_orden('NORMAL')
                play(audios_folder + 'orden_normal.wav')
                return
            if ('invertido' in message) or ('uno' in message):
                cambiar_orden('INVERTIDO')
                play(audios_folder + 'orden_invertido.wav')
                return

        if ('cambiar' in message) or ('velocidad' in message):
            if ('normal' in message) or ('cero' in message):
                cambiar_velocidad('NORMAL')
                play(audios_folder + 'velocidad_normal.wav')
                return
            if ('aumentada' in message) or ('uno' in message):
                cambiar_velocidad('AUMENTADA')
                play(audios_folder + 'velocidad_aumentada.wav')
                return

        if ('remover' in message) or ('parte' in message):
            if ('ninguna' in message) or ('cero' in message):
                cambiar_remover_parte('NINGUNA')
                play(audios_folder + 'remover_normal.wav')
                return
            if ('inicial' in message) or ('uno' in message):
                cambiar_remover_parte('INICIAL')
                play(audios_folder + 'remover_inicio.wav')
                return
            if ('media' in message) or ('dos' in message):
                cambiar_remover_parte('MEDIA')
                play(audios_folder + 'remover_medio.wav')
                return
            if ('final' in message) or ('tres' in message):
                cambiar_remover_parte('FINAL')
                play(audios_folder + 'remover_final.wav')
                return
        print "Comando aplicado"

    # Sofia, puedes ayudarme a ver qué opciones tengo seleccionadas
    if (u'sofía' in message) or ('puedes' in message) or ('ayudarme' in message) or ('ver' in message) or ('seleccionados' in message):
        comandos_seleccionados()
        return

    if ('describir' in message) or (u'opción' in message):
        play(audios_folder + 'lista_comandos.wav')
        return

    if message == COMANDO_INVALIDO or not message.strip():
        print COMANDO_INVALIDO
        return
    speedup(VELOCIDAD)
    reverse(ORDEN)
    remover_parte(REMOVER_PARTE)
    play()
    return

def transcripts_from_response(response):
    x = json.loads(response.text)
    if 'results' in x:
        transcripts = [ r['alternatives'][0]['transcript'] for r in x['results'] ]
        return ' '.join(transcripts)
    else:
        return COMANDO_INVALIDO

def asr(filename):
    with open(filename, 'rb') as data:
        headers = {
            'Content-Type': 'audio/wav',
        }

        params = (
            ('model', 'es-ES_BroadbandModel'),
        )

        r = requests.post('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize', headers=headers, params=params, data=data, auth=('c2bd3588-ad8d-4405-a1c8-28ffde7beaee', 'wNINKHokHL1w'))
        return transcripts_from_response(r)

def cambiar_velocidad(nueva_velocidad):
    global VELOCIDAD
    VELOCIDAD = nueva_velocidad
    print "Nueva velocidad: " + VELOCIDAD

def cambiar_orden(nuevo_orden):
    global ORDEN
    ORDEN = nuevo_orden
    print "Nueva orden: " + ORDEN

def cambiar_remover_parte(nueva_parte):
    global REMOVER_PARTE
    REMOVER_PARTE = nueva_parte
    print "Remover nueva parte: " + REMOVER_PARTE
