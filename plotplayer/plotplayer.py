import matplotlib.pylab as pylab

from matplotlib.animation import FuncAnimation

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
    _playing = False

    def __init__(self, windowTitle=None, figure=None, windowSize=DEFAULT_WINDOW_SIZE, sliderBackgroundColor=renderHandler.SLIDER_BACKGROUND_COLOR,
                toolbarVisible=False, sliderVisible=True, keyPressHandler=None, skipSize=inputHandler.SKIP_SIZE, jumpSize=inputHandler.JUMP_SIZE):
        if figure == None:
            figure = pylab.plt.figure(figsize=windowSize)
        typeValidation.assertIsFigure(figure, 'figure')
        self._figure = figure

        if windowTitle == None:
            windowTitle = DEFAULT_ANIMATION_NAME
        figure.canvas.set_window_title(windowTitle)

        animationAxes = None
        sliderAxes = None
        if len(figure.axes) > 0:
            animationAxes = figure.axes[0]
        if len(figure.axes) > 1:
            sliderAxes = figure.axes[1]
        self._renderHandler = renderHandler.RenderHandler(figure, animationAxes, sliderAxes, sliderBackgroundColor, sliderVisible, toolbarVisible)

        self._inputHandler = inputHandler.InputHandler(self, keyPressHandler, skipSize, jumpSize)

    def initializeAnimation(self, totalFrames, drawFunc, animationName=DEFAULT_ANIMATION_NAME, frameRate=30):
        typeValidation.assertIsInt(totalFrames, 'totalFrames')
        typeValidation.assertIsFunction(drawFunc, 'drawFunc')
        typeValidation.assertIsInt(frameRate, 'frameRate')

        self.stop()
        self._renderHandler.initializeRendering(totalFrames, drawFunc)
        self._inputHandler.setEnabled(True)

        self._animationName = animationName
        self._frameRate = frameRate
        self._playing = False

    def render(self, frameNumber):
        self._renderHandler.render(frameNumber)

        if frameNumber == self.getTotalFrames():
            self.stop()

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

    def getFigure(self):
        return self._figure

    def getCurrentFrameNumber(self):
        return int(self._renderHandler._slider.val)

    def getTotalFrames(self):
        return int(self._renderHandler._slider.valmax)

    def toggleToolbar(self):
        self._renderHandler.toggleToolbar()

    def toggleSlider(self):
        self._renderHandler.toggleSlider()

    def getHtml(self):
        html = self._animation.to_html5_video()
        return html

    def getJavascript(self):
        javascript = self._animation.to_jshtml()
        return javascript

    def saveVideo(self, fileName=None, writer=None):
        self.stop()

        if fileName == None:
            fileName = uiHelper.getSaveDialogResult(SAVE_DIALOG_TITLE, self._animationName + VIDEO_EXTENSION,
                                                    [ VIDEO_FILE_TYPE, uiHelper.ALL_FILES_TYPE ], VIDEO_EXTENSION)
        self._animation.save(fileName, writer)

    def saveHtml(self, fileName=None):
        self.stop()

        if fileName == None:
            fileName = uiHelper.getSaveDialogResult(SAVE_DIALOG_TITLE, self._animationName + HTML_EXTENSION,
                                                   [ HTML_FILE_TYPE, uiHelper.ALL_FILES_TYPE ], HTML_EXTENSION)
        videoHtml = self.getHtml()
        fileHelper.saveFile(fileName, videoHtml)

    def saveJavascript(self, fileName=None):
        self.stop()

        if fileName == None:
            fileName = uiHelper.getSaveDialogResult(SAVE_DIALOG_TITLE, self._animationName + JAVASCRIPT_EXTENSION,
                                                   [ JAVASCRIPT_FILE_TYPE, uiHelper.ALL_FILES_TYPE ], JAVASCRIPT_EXTENSION)
        videoJavascript = self.getJavascript()
        fileHelper.saveFile(fileName, videoJavascript)

    @staticmethod
    def showPlayers(blocking=True):
        uiHelper.showPlayers(blocking)