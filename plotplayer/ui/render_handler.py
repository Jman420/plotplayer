from matplotlib.widgets import Slider
from tkinter.constants import BOTTOM, X

IMAGE_AXES_RECT = [0, 0.03, 1, 0.97]  # [ x, y, width, height ] in percentage of window size
SLIDER_AXES_RECT = [0, 0, 1, 0.03]  # [ x, y, width, height ] in percentage of window size
SLIDER_BACKGROUND_COLOR = 'lightgoldenrodyellow'

DEFAULT_FRAME_RATE = 30

class RenderHandler(object):
    """Render Handler for PlotPlayer Viewer"""

    _playerFigure = None
    _animationAxes = _renderFunc = None
    _sliderAxes = _slider = None
    _sliderVisible = _toolbarVisible = False

    def __init__(self, playerFigure, animationAxes=None, sliderAxes=None, sliderBackgroundColor=SLIDER_BACKGROUND_COLOR,
                sliderVisible=True, toolbarVisible=False):
        self._playing = False
        self._playerFigure = playerFigure

        if animationAxes == None:
            animationAxes = self._playerFigure.add_axes(IMAGE_AXES_RECT)
            animationAxes.set_axis_off()
        self._animationAxes = animationAxes

        if sliderAxes == None:
            sliderAxes = self._playerFigure.add_axes(SLIDER_AXES_RECT, facecolor=sliderBackgroundColor)
        self._sliderAxes = sliderAxes

        self.setSliderVisible(sliderVisible)
        self.setToolbarVisible(toolbarVisible)

    def initializeRendering(self, totalFrames, renderFunc):
        self._slider = Slider(self._sliderAxes, str(), 0, totalFrames - 1, valinit=0.0)
        self._slider.on_changed(self.handleSliderChanged)

        self._renderFunc = renderFunc

    def render(self, frameNumber):
        frameNumber = min(max(0, int(frameNumber)), self._slider.valmax)

        self.renderSlider(frameNumber)
        self.renderImage(frameNumber)

    def renderImage(self, frameNumber):
        self._playerFigure.sca(self._animationAxes)
        self._renderFunc(frameNumber, self._animationAxes)
        self._playerFigure.canvas.draw_idle()

    def renderSlider(self, newSliderVal):
        currentFrameNumber = int(self._slider.val)
        if currentFrameNumber != newSliderVal:
            self._slider.set_val(newSliderVal)

    def handleSliderChanged(self, sliderValue):
        self.render(sliderValue)

    def setSliderVisible(self, visible):
        self._sliderAxes.set_visible(visible)
        self._playerFigure.canvas.draw()
        self._sliderVisible = visible

    def toggleSlider(self):
        self.setSliderVisible(not self._sliderVisible)

    def setToolbarVisible(self, visible):
        if visible:
            self._playerFigure.canvas.toolbar.pack(side=BOTTOM, fill=X)
        else:
            self._playerFigure.canvas.toolbar.pack_forget()

        self._toolbarVisible = visible

    def toggleToolbar(self):
        self.setToolbarVisible(not self._toolbarVisible)