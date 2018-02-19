import matplotlib.pylab as pylab

from matplotlib.animation import FuncAnimation
import tkinter.constants as Tkinter

import typeValidation
import helpers.fileHelper as fileHelper
import helpers.uiHelper as uiHelper
import ui.renderHandler as renderHandler
import ui.inputHandler as inputHandler

DEFAULT_WINDOW_SIZE = (8, 4.5)  # Aspect ratio (ie. 4:3, 16:9, 21:9) in relation to DPI; default is half 16:9 (8:4.5)
DEFAULT_ANIMATION_NAME = 'PlotPlayer'

VIDEO_EXTENSION = '.mp4'
HTML_EXTENSION = '.html'
JAVASCRIPT_EXTENSION = '.js.html'

SAVE_DIALOG_TITLE = 'Select video file to save'

VIDEO_FILE_TYPE = [ 'MP4 Video', '*{}'.format(VIDEO_EXTENSION) ]
HTML_FILE_TYPE = [ 'HTML File', '*{}'.format(HTML_EXTENSION) ]
JAVASCRIPT_FILE_TYPE = [ 'Javascript HTML File', '*{}'.format(JAVASCRIPT_EXTENSION) ]

class PlotPlayer(object):
    '''Function based animation player for Matplotlib'''
    _figure = None
    _renderHandler = _inputHandler = None
    _animationName = _animation = None
    _frameRate = None
    _playing = _toolbarVisible = False

    def __init__(self, windowTitle=None, figure=None, windowSize=DEFAULT_WINDOW_SIZE, sliderBackgroundColor=renderHandler.SLIDER_BACKGROUND_COLOR,
                toolbarVisible=False, sliderVisible=True, keyPressHandler=None, skipSize=inputHandler.SKIP_SIZE, jumpSize=inputHandler.JUMP_SIZE):
        if figure == None:
            figure = pylab.plt.figure(figsize=windowSize)
        typeValidation.assertIsFigure(figure, 'figure')
        self._figure = figure

        self.setToolbarVisible(toolbarVisible)

        if windowTitle == None:
            windowTitle = DEFAULT_ANIMATION_NAME
        figure.canvas.set_window_title(windowTitle)

        animationAxes = None
        sliderAxes = None
        if len(figure.axes) > 0:
            animationAxes = figure.axes[0]
        if len(figure.axes) > 1:
            sliderAxes = figure.axes[1]
        self._renderHandler = renderHandler.RenderHandler(figure, animationAxes, sliderAxes, sliderBackgroundColor, sliderVisible)

        self._inputHandler = inputHandler.InputHandler(self, keyPressHandler, skipSize, jumpSize)

    def initializeAnimation(self, totalFrames, drawFunc, animationName=DEFAULT_ANIMATION_NAME, frameRate=30):
        typeValidation.assertIsInt(totalFrames, 'totalFrames')
        typeValidation.assertIsFunction(drawFunc, 'drawFunc')
        typeValidation.assertIsInt(frameRate, 'frameRate')

        self.stop()
        self._renderHandler.initializeRendering(totalFrames, drawFunc)

        self._animationName = animationName
        self._frameRate = frameRate
        self._playing = False

    def render(self, frameNumber):
        self._renderHandler.render(frameNumber)

    def play(self):
        if self._playing:
            return

        slider = self._renderHandler._slider
        if slider.val == slider.valmax:
            self.render(0)

        framesToPlay = range(int(slider.val), slider.valmax + 1)
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

    def setToolbarVisible(self, visible):
        if visible:
            self._figure.canvas.toolbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        else:
            self._figure.canvas.toolbar.pack_forget()

        self._toolbarVisible = visible

    def toggleToolbar(self):
        self.setToolbarVisible(~self._toolbarVisible)

    def getHtml(self):
        html = self._animation.to_html5_video()
        return html

    def getJavascript(self):
        javascript = self._animation.to_jshtml()
        return javascript

    def saveVideo(self, defaultFileName, writer=None):
        self.stop()

        saveFileName = uiHelper.getSaveDialogResult(SAVE_DIALOG_TITLE, defaultFileName,
                                                   [ VIDEO_FILE_TYPE, uiHelper.ALL_FILES_TYPE ], VIDEO_EXTENSION)
        self._animation.save(saveFileName, writer)

    def saveHtml(self, defaultFileName):
        self.stop()

        saveFileName = uiHelper.getSaveDialogResult(SAVE_DIALOG_TITLE, defaultFileName,
                                                   [ HTML_FILE_TYPE, uiHelper.ALL_FILES_TYPE ], HTML_EXTENSION)
        videoHtml = self.getHtml()
        fileHelper.saveFile(saveFileName, videoHtml)

    def saveJavascript(self, defaultFileName):
        self.stop()

        saveFileName = uiHelper.getSaveDialogResult(SAVE_DIALOG_TITLE, defaultFileName,
                                                   [ JAVASCRIPT_FILE_TYPE, uiHelper.ALL_FILES_TYPE ], JAVASCRIPT_EXTENSION)
        videoJavascript = self.getJavascript()
        fileHelper.saveFile(saveFileName, videoJavascript)

    @staticmethod
    def showPlayers(blocking=True):
        uiHelper.showPlayers(blocking)