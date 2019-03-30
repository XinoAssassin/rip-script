# -*- coding: UTF-8 –*-
import vapoursynth as vs
import sys
import mvsfunc as mvf
import havsfunc as haf

core = vs.get_core(__threads__)
core.max_cache_size = 14000

source = r"__filename__"
src = core.lsmas.LWLibavSource(source, threads=__threads__, format="YUV420P8")

#change depth
p16 = mvf.Depth(src, depth=16)

#deint
deint = core.yadifmod.Yadifmod(clip=p16, edeint=core.nnedi3.nnedi3(clip=p16, field=1), order=1, field=-1, mode=0, opt=4)

deint.set_output()