#!usr/bin/env python

from pydub import AudioSegment
import sys
from TTS_and_STT import text_to_speech

text_to_speech("prueba2.wav", "esto es una prueba", rate_change="+0%", f0mean_change="+0%")
