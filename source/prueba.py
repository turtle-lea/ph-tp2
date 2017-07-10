#!usr/bin/env python

from pydub import AudioSegment
import sys

song = AudioSegment.from_wav("../audios/describir_velocidad.wav")
three_seconds = 3 * 1000
first_3_seconds = song[:three_seconds]
# last_3_seconds = song[-3000:]

# # boost volume by 6dB
# beginning = first_10_seconds + 6
# # reduce volume by 3dB
# end = last_5_seconds - 3

# x = sys.argv[1]

# print "Hola"

(first_3_seconds * 2).export("modified.wav", format="wav")

# (first_3_seconds + last_3_seconds).export("modified.wav", format="wav")

# forward.export("modified.wav", format="wav")
