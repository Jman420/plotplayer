from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

IMAGE_AXES_RECT = [0, 0.03, 1, 0.97]  # [ x, y, width, height ] in percentage of window size
SLIDER_AXES_RECT = [0, 0, 1, 0.03]  # [ x, y, width, height ] in percentage of window size
SLIDER_BACKGROUND_COLOR = 'lightgoldenrodyellow'

DEFAULT_FRAME_RATE = 30

class AnimationHandler(object):
    """Animation Handler for PlotPlayer Viewer"""

    _playerFigure = None
    _totalFrames = _frameRate = None
    _animationAxes = _animationFunc = None
    _sliderAxes = _slider = None
    _playing = False

    def __init__(self, playerFigure, animationAxes=None, sliderAxes=None, sliderBackgroundColor=SLIDER_BACKGROUND_COLOR,
                hideSlider=False):
        self._playing = False
        self._playerFigure = playerFigure
        self._frameRate = frameRate

        if animationAxes == None:
            animationAxes = self._playerFigure.add_axes(IMAGE_AXES_RECT)
            animationAxes.set_axis_off()
        self._animationAxes = animationAxes

        if sliderAxes == None:
            sliderAxes = self._playerFigure.add_axes(SLIDER_AXES_RECT, facecolor=sliderBackgroundColor)
        self._sliderAxes = sliderAxes

        self._slider = Slider(self._sliderAxes, '', 0, 1, valinit=0.0)
        self._slider.on_changed(self.handleSliderChanged)

        if hideSlider:
            self.setSliderVisible(False)

    def initializeAnimation(self, totalFrames, drawFunc):
        self._totalFrames = totalFrames
        self._animationFunc = drawFunc

    def render(self, frameNumber):
        frameNumber = min(max(0, int(frameNumber)), self._totalFrames)
        self.renderSlider(frameNumber)
        self.renderImage(frameNumber)

    def renderImage(self, frameNumber):
        self._playerFigure.sca(self._animationAxes)
        self._animationFunc(frameNumber, self._animationAxes)
        self._playerFigure.canvas.draw_idle()

    def renderSlider(self, newSliderVal):
        if newSliderVal <= self._slider.valmax:
            self._slider.set_val(newSliderVal)

    def handleSliderChanged(self, sliderValue):
        sliderFrameNumber = int(self._totalFrames * sliderValue)
        self.render(sliderFrameNumber)