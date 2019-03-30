# -*- coding: UTF-8 –*-
import vapoursynth as vs
import sys
import mvsfunc as mvf
import havsfunc as haf

core = vs.get_core(__threads__)
core.max_cache_size = 14000

source = r"__filename__"
src = core.ffms2.source(source, threads=__threads__)
#change depth
p16 = mvf.Depth(src, depth=16)

p16.set_output()