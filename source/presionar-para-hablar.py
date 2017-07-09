#!/usr/bin/env python
# coding=utf-8

# https://pypi.python.org/pypi/pynput
from pynput import mouse
import recorder
import time
from dialog_management import manage

recfile = None
grabando = False

def on_click(x, y, button, pressed):
  global grabando, recfile

  # Presionar el botón izquierdo para empezar a grabar.
  if pressed and button==mouse.Button.left:
    if not grabando:
      print 'Empieza grabacion'
      recfile = recorder.Recorder(channels=2).open('audio.wav', 'wb')
      grabando = True
      recfile.start_recording()

  # Soltar el botón izquierdo para dejar de grabar.
  if not pressed and button==mouse.Button.left:
    if grabando:
      print 'Termina grabacion'
      recfile.stop_recording()
      recfile = None
      grabando = False
      manage()
      # Acá ya se podría hacer algo con el archivo creado.

  # Presionar el botón derecho para terminar.
  if pressed and button==mouse.Button.right:
    if not grabando:
      return False

with mouse.Listener(on_click=on_click) as listener:
  listener.join()
