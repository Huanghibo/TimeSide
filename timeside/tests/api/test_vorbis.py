# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *

source = "../samples/sweep.wav"
dest = "../results/sweep_wav.ogg"

decoder  = FileDecoder(source)
encoder  = VorbisEncoder(dest)

(decoder | encoder).run()
