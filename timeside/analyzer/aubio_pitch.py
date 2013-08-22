# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Paul Brossier <piem@piem.org>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Paul Brossier <piem@piem.org>

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import *
from timeside.api import IValueAnalyzer
from aubio import pitch

class AubioPitch(Analyzer):
    implements(IAnalyzer) # TODO check if needed with inheritance

    def __init__(self):
        self.input_blocksize = 2048
        self.input_stepsize = self.input_blocksize / 2

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioPitch, self).setup(channels, samplerate, blocksize, totalframes)
        self.p = pitch("default", self.input_blocksize, self.input_stepsize,
                       samplerate)
        self.p.set_unit("freq")
        self.block_read = 0
        self.pitches = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_pitch_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "f0 (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "pitch values"

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.input_stepsize):
            #time = self.block_read * self.input_stepsize * 1. / self.samplerate()
            self.pitches += [self.p(samples)[0]]
            self.block_read += 1
        return frames, eod

    def results(self):

        container = super(AubioPitch, self).results()

        pitch = self.new_result(dataMode='value', resultType='framewise')

        pitch.idMetadata.id = "aubio_pitch"
        pitch.idMetadata.name = "f0 (aubio)"
        pitch.idMetadata.unit = 'Hz'

        # parameters : None # TODO check with Piem "default" and "freq" in setup

        # Set Data
        self.pitches = numpy.array(self.pitches)
        pitch.data.data = self.pitches
        pitch.data.dataType = float
        container.add_result(pitch)

        return container