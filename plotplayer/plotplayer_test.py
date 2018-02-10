from plotplayer.plotplayer import plotplayer
import numpy as np
import matplotlib.pylab as pylab
import matplotlib.pyplot as pyplot

def redraw_fn(f, axes):
    amp = float(f) / 3000
    f0 = 3
    t = np.arange(0.0, 1.0, 0.001)
    s = amp * np.sin(2 * np.pi * f0 * t)
    if not redraw_fn.initialized:
        redraw_fn.l, = axes.plot(t, s, lw=2, color='red')
        redraw_fn.initialized = True
    else:
        redraw_fn.l.set_ydata(s)
redraw_fn.initialized = False

video1 = plotplayer()
video1.hideToolbar()
video1.initializeAnimation(100, redraw_fn)
video1.play()

#video1.saveAnimationVideo("C:\\temp\\dummy.mp4")
#video1.saveHtml("C:\\temp\\dummy-html.html")

video1.show()