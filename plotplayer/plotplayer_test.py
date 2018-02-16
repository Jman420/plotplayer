import numpy

from plotplayer import PlotPlayer

def redraw_fn(frameNumber, axes):
    amp = float(frameNumber) / 3000
    f0 = 3
    t = numpy.arange(0.0, 1.0, 0.001)
    s = amp * numpy.sin(2 * numpy.pi * f0 * t)
    if not redraw_fn.initialized:
        redraw_fn.l, = axes.plot(t, s, lw=2, color='red')
        redraw_fn.initialized = True
    else:
        redraw_fn.l.set_ydata(s)
redraw_fn.initialized = False

video1 = PlotPlayer()
video1.hideToolbar()
video1.initializeAnimation(100, redraw_fn)
video1.play()

PlotPlayer.showPlayers()