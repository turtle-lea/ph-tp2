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
COMANDO_INVALIDO = "Ingrese audio nuevamente"

# VELOCIDAD. Estados: NORMAL, AUMENTADA
VELOCIDAD = "NORMAL"

# ORDEN. Estados: NORMAL, INVERTIDO
ORDEN = "NORMAL"

# REMOVER_PARTE. Estados: NINGUNA, INICIAL, MEDIA, FINAL
REMOVER_PARTE = "NINGUNA"

# FILTRO_PASABAJOS. Estados: NORMAL, ACTIVADO
FILTRO_PASABAJOS = "NORMAL"

# REPETIR_CICLO. Estados: NORMAL, ACTIVADO
REPETIR_CICLO = "NORMAL"

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
    return

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
    if remover_parte == "NINGUNA":
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

def filtrar_bajos(filtro_pasabajos):
    global audios_folder
    if filtro_pasabajos == "NORMAL":
        return
    audio = AudioSegment.from_wav("audio.wav")
    two_seconds = 2*1000
    audio_muy_corto = audios_folder + 'audio_muy_corto.wav'
    if audio.duration_seconds < 4 and filtro_pasabajos != "NORMAL":
        play(audio_muy_corto)
        return
    beginning = audio[:two_seconds]
    beginning.append(audio[two_seconds:].low_pass_filter(150)).export("audio.wav", format="wav")
    return

def repetir_ciclo(modo_repeticion):
    if modo_repeticion == "NORMAL":
        return
    audio = AudioSegment.from_wav("audio.wav")
    (audio * 3).export("audio.wav", format="wav")
    return

def comandos_seleccionados():
    global VELOCIDAD, ORDEN, REMOVER_PARTE
    text = " Por supuesto. Velocidad: " + VELOCIDAD + ". Orden: " + ORDEN + ". Remover parte: " + REMOVER_PARTE + ". Filtro pasabajos: " + FILTRO_PASABAJOS + ". Repetir ciclo: " + REPETIR_CICLO
    text_to_speech("comandos_seleccionados.wav", text, rate_change="+0%", f0mean_change="+0%")
    play("comandos_seleccionados.wav")
    return

def manage():
    global VELOCIDAD, ORDEN, REMOVER_PARTE, COMANDO_INVALIDO, FILTRO_PASABAJOS, REPETIR_CICLO
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
        if ('filtro' in message) or ('pasa' in message) or ('bajos' in message):
            if ('normal' in message) or ('cero' in message):
                cambiar_filtro_pasabajos('NORMAL')
                play(audios_folder + 'pasabajos_normal.wav')
                return
            if ('activado' in message) or ('uno' in message):
                cambiar_filtro_pasabajos('ACTIVADO')
                play(audios_folder + 'pasabajos_activado.wav')
                return

        if ('repetir' in message) or ('ciclo' in message):
            if ('normal' in message) or ('cero' in message):
                cambiar_repetir_ciclo('NORMAL')
                play(audios_folder + 'repetir_ciclo_normal.wav')
                return
            if ('activado' in message) or ('uno' in message):
                cambiar_repetir_ciclo('ACTIVADO')
                play(audios_folder + 'repetir_ciclo_activado.wav')
                return

        play(audios_folder + 'repetir_nuevamente.wav')
        return

    # Sofia, puedes ayudarme a ver qué opciones tengo seleccionadas
    if (u'sofía' in message) or ('puedes' in message) or ('ayudarme' in message) or ('recordar' in message) or ('seleccionadas' in message):
        comandos_seleccionados()
        return

    if ('describir' in message) or (u'uso' in message):
        if ('cambiar' in message) or ('velocidad' in message):
            play(audios_folder + 'describir_velocidad.wav')
            return
        if ('modificar' in message) or ('orden' in message):
            play(audios_folder + 'describir_orden.wav')
            return
        if ('remover' in message) or ('parte' in message):
            play(audios_folder + 'describir_remover_parte.wav')
            return
        if ('filtro' in message) or ('pasa' in message) or ('bajos') in message:
            play(audios_folder + 'describir_filtro_pasabajos.wav')
            return
        if ('repetir' in message) or ('ciclo' in message):
            play(audios_folder + 'describir_repetir_ciclo.wav')
            return
        play(audios_folder + 'repetir_nuevamente.wav')
        return

    if message == COMANDO_INVALIDO or not message.strip():
        print COMANDO_INVALIDO
        return
    speedup(VELOCIDAD)
    reverse(ORDEN)
    filtrar_bajos(FILTRO_PASABAJOS)
    remover_parte(REMOVER_PARTE)
    repetir_ciclo(REPETIR_CICLO)
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
    return

def cambiar_orden(nuevo_orden):
    global ORDEN
    ORDEN = nuevo_orden
    print "Nueva orden: " + ORDEN
    return

def cambiar_remover_parte(nueva_parte):
    global REMOVER_PARTE
    REMOVER_PARTE = nueva_parte
    print "Remover nueva parte: " + REMOVER_PARTE
    return

def cambiar_filtro_pasabajos(nueva_filtro):
    global FILTRO_PASABAJOS
    FILTRO_PASABAJOS = nueva_filtro
    print "Filtro pasabajos: " + FILTRO_PASABAJOS
    return

def cambiar_repetir_ciclo(nuevo_ciclo):
    global REPETIR_CICLO
    REPETIR_CICLO = nuevo_ciclo
    print "Repetir ciclo: " + REPETIR_CICLO
    return
