import matplotlib
import matplotlib.pylab as pylab

import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.figure import Figure
import tkinter.constants as Tkinter

def saveFile(fileName, data):
    file = open(fileName, 'w')
    file.write(data)
    file.close()

def assertIsFigure(value, variableName):
    assert isinstance(value, Figure), variableName + ' must be an instance of ' + str(Figure)

def assertIsInt(value, variableName):
    assert isinstance(value, int), variableName + ' must be an instance of ' + str(int) 

def assertIsFunction(value, variableName):
    assert callable(value), name + ' must be a callable function'

class plotplayer(object):
    '''Lightweight function based animation player for Matplotlib'''

    IMAGE_AXES_RECT = [0, 0.03, 1, 0.97]  # [ x, y, width, height ] in percentage of window size
    SLIDER_AXES_RECT = [0, 0, 1, 0.03]  # [ x, y, width, height ] in percentage of window size

    _figure = _animationName = None
    _animationAxes = _drawFunc = None
    _sliderAxes = _slider = None
    _animation = _playing = None
    _frameRate = None
    _toolbarHidden = _playing = False

    def __init__(self, windowTitle=None, figure=None, sliderBackgroundColor='lightgoldenrodyellow', hideToolbar=True):
        if figure == None:
            figure = pylab.plt.figure()
        assertIsFigure(figure, 'figure')

        if not windowTitle == None:
            figure.canvas.set_window_title(windowTitle)

        if len(figure.axes) > 0:
            animationAxes = figure.gca()
        else:
            animationAxes = figure.add_axes(self.IMAGE_AXES_RECT)
            animationAxes.set_axis_off()

        sliderAxes = figure.add_axes(self.SLIDER_AXES_RECT, facecolor=sliderBackgroundColor)

        self._figure = figure
        self._animationAxes = animationAxes
        self._sliderAxes = sliderAxes

        if hideToolbar:
            self.hideToolbar()

    def initializeAnimation(self, totalFrames, drawFunc, animationName='plotplayer', frameRate=30):
        assertIsInt(totalFrames, 'totalFrames')
        assertIsFunction(drawFunc, 'drawFunc')
        assertIsInt(frameRate, 'frameRate')

        slider = Slider(self._sliderAxes, '', 0, totalFrames - 1, valinit=0.0)
        slider.on_changed(self.render)
        
        self._animationName = animationName
        self._figure.canvas.mpl_connect('button_press_event', self.handleMouseButtonDown)
        self._figure.canvas.mpl_connect('key_press_event', self.handleKeyPress)

        self._playing = False
        self._drawFunc = drawFunc
        self._slider = slider
        self._frameRate = frameRate

    def render(self, frameNumber):
        frameNumber = min(max(0, int(frameNumber)), self._slider.valmax)
        self.renderSlider(frameNumber)
        self.renderImage(frameNumber)

    def renderImage(self, frameNumber):
        self._figure.sca(self._animationAxes)
        self._drawFunc(frameNumber, self._animationAxes)
        self._figure.canvas.draw_idle()

    def renderSlider(self, newFrameNumber):
        currentFrameNumber = int(self._slider.val)
        if currentFrameNumber != newFrameNumber:
            self._slider.set_val(newFrameNumber)

        if newFrameNumber == self._slider.valmax:
            self.stop()

    def show(self, blocking=True):
        try:
            pylab.plt.show(blocking)
        except AttributeError:
            print('Videofig encountered a playback error.')
            print('This is usually due to a videofig window getting closed during animation playback...')
            print('This causes all open videofig windows to malfunction.')
            print('Closing all videofig windows...')
            pylab.plt.close('all')
            pass

    def play(self):
        if self._playing:
            return

        framesToPlay = range(int(self._slider.val), self._slider.valmax + 1)
        animation = FuncAnimation(self._figure, self.render, framesToPlay, interval=1000 // self._frameRate, repeat=False)
        self._figure.canvas.draw()

        self._playing = True
        self._animation = animation

    def stop(self):
        if not self._playing:
            return

        self._animation.event_source.stop()
        self._playing = False

    def togglePlayback(self):
        if self._playing:
            self.stop()
        else:
            self.play()

    def hideToolbar(self):
        self._figure.canvas.toolbar.pack_forget()
        self._toolbarHidden = True

    def showToolbar(self):
        self._figure.canvas.toolbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        self._toolbarHidden = False

    def toggleToolbar(self):
        if self._toolbarHidden:
            self.showToolbar()
        else:
            self.hideToolbar()

    def handleKeyPress(self, eventData):
        key = eventData.key
        currentFrame = int(self._slider.val)



        if key in [ 'left', 'right', 'end', 'home' ]:
            self.stop()

        if key == 'left':
            self.render(currentFrame - 1)
        elif key == 'right':
            self.render(currentFrame + 1)
        elif key == 'end':
            self.render(self._slider.valmax)
        elif key == 'home':
            self.render(0)
        elif key in [ ' ', 'enter' ]:
            self.togglePlayback()
        elif key == 't':
            self.toggleToolbar()

    def handleMouseButtonDown(self, eventData):
        if eventData.inaxes == self._sliderAxes:
            self.stop()

    def getHtml(self):
        html = self._animation.to_html5_video()
        return html

    def getJavascript(self):
        javascript = self._animation.to_jshtml()
        return javascript

    def saveVideo(self, fileName, writer=None):
        self._animation.save(fileName, writer)

    def saveHtml(self, fileName):
        videoHtml = self.getHtml()
        saveFile(fileName, videoHtml)

    def saveJavascript(self, fileName):
        videoJavascript = self.getJavascript()
        saveFile(fileName, videoJavascript)