import helpers.uiHelper as uiHelper

SKIP_BACK_BUTTON = 'left'
SKIP_AHEAD_BUTTON = 'right'
JUMP_BACK_BUTTON = 'down'
JUMP_AHEAD_BUTTON = 'up'
TOGGLE_PLAY_BUTTON = [ ' ', 'enter' ]
GOTO_BEGINNING_BUTTON = 'home'
GOTO_END_BUTTON = 'end'
TOGGLE_SLIDER_BUTTON = 't'
TOGGLE_TOOLBAR_BUTTON = 'm'
SAVE_BUTTON = 'd'
SAVE_VIDEO_BUTTON = 'v'
SAVE_HTML_BUTTON = 'h'
SAVE_JAVASCRIPT_BUTTON = 'j'

KEYS_TRIGGER_STOP = [ SKIP_BACK_BUTTON, SKIP_AHEAD_BUTTON, JUMP_BACK_BUTTON, JUMP_AHEAD_BUTTON,
                     GOTO_BEGINNING_BUTTON, GOTO_END_BUTTON ]

SKIP_SIZE = 1
JUMP_SIZE = 10

class InputHandler(object):
    """User Input Handler for PlotPlayer Windows"""

    _plotPlayer = None
    _handlerEnabled = False
    _keyPressHandler = None
    _saveButtonPressed = False
    _skipSize = _jumpSize = None

    def __init__(self, plotPlayer, keyPressHandler=None, skipSize=SKIP_SIZE, jumpSize=JUMP_SIZE, enabled=False):
        self._plotPlayer = plotPlayer
        self._skipSize = skipSize
        self._jumpSize = jumpSize
        self._saveButtonPressed = False
        self.setEnabled(enabled)

        canvas = self._plotPlayer._figure.canvas
        canvas.mpl_connect('button_press_event', self.handleMouseButtonDown)
        canvas.mpl_connect('key_press_event', self.handleKeyPress)
        canvas.mpl_connect('key_release_event', self.handleKeyRelease)

    def handleKeyPress(self, eventData):
        if not self._handlerEnabled:
            return

        if not self._keyPressHandler == None and self._keyPressHandler(eventData):
            return
        
        plotPlayer = self._plotPlayer
        key = eventData.key
        if self._saveButtonPressed:
            animationName = plotPlayer._animationName
            if key == SAVE_VIDEO_BUTTON:
                plotPlayer.saveVideo(animationName + VIDEO_EXTENSION)
            elif key == SAVE_HTML_BUTTON:
                plotPlayer.saveHtml(animationName + HTML_EXTENSION)
            elif key == SAVE_JAVASCRIPT_BUTTON:
                plotPlayer.saveJavascript(animationName + JAVASCRIPT_EXTENSION)

        if key in KEYS_TRIGGER_STOP:
            plotPlayer.stop()

        currentFrame = int(self._slider.val)
        if key == SKIP_BACK_BUTTON:
            plotPlayer.render(currentFrame - self._skipSize)
        elif key == SKIP_AHEAD_BUTTON:
            plotPlayer.render(currentFrame + self._skipSize)
        elif key == JUMP_BACK_BUTTON:
            plotPlayer.render(currentFrame - self._jumpSize)
        elif key == JUMP_AHEAD_BUTTON:
            plotPlayer.render(currentFrame + self._jumpSize)
        elif key == GOTO_BEGINNING_BUTTON:
            plotPlayer.render(0)
        elif key == GOTO_END_BUTTON:
            plotPlayer.render(self._slider.valmax)
        elif key == TOGGLE_SLIDER_BUTTON:
            plotPlayer.toggleSlider()
        elif key in TOGGLE_PLAY_BUTTON:
            plotPlayer.togglePlayback()
        elif key == TOGGLE_TOOLBAR_BUTTON:
            plotPlayer.toggleToolbar()
        elif key == SAVE_BUTTON:
            self._saveButtonPressed = True

    def handleKeyRelease(self, eventData):
        if not self._handlerEnabled:
            return

        key = eventData.key

        if key == SAVE_BUTTON:
            self._saveButtonPressed = False

    def handleMouseButtonDown(self, eventData):
        if not self._handlerEnabled:
            return

        plotPlayer = self._plotPlayer
        if eventData.inaxes == plotPlayer._sliderAxes:
            plotPlayer.stop()

    def setEnabled(self, enabled):
        self._handlerEnabled = enabled