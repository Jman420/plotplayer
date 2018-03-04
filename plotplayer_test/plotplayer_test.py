import numpy

from plotplayer.plotplayer import PlotPlayer


def redraw_fn(frame_num, axes):
    amp = float(frame_num) / 3000
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
video1.initialize(100, redraw_fn)
video1.get_render_manager().set_limits([-0.05, 1.05], [-0.05, 0.05])
#video1.get_animation_manager().render(0)
#video1.play()

PlotPlayer.show_players()
