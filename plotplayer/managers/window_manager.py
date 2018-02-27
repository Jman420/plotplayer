from tkinter.constants import BOTTOM, X
from matplotlib import pyplot

from ..validators import type_validation

# Aspect ratio (ie. 4:3, 16:9, 21:9) in relation to DPI; default is half 16:9 (8:4.5)
DEFAULT_WINDOW_SIZE = (8, 4.5)
DEFAULT_ANIMATION_NAME = 'PlotPlayer'

class WindowManager(object):
    """description of class"""

    _figure = None
    _toolbar_visible = False

    def __init__(self, window_size=DEFAULT_WINDOW_SIZE, window_title=DEFAULT_ANIMATION_NAME,
                 figure=None, toolbar_visible=True):
        if figure is None:
            figure = pyplot.figure(figsize=window_size)
        type_validation.assert_is_figure(figure, 'figure')
        self._figure = figure

        if window_title is None:
            window_title = DEFAULT_ANIMATION_NAME
        figure.canvas.set_window_title(window_title)

        self.set_toolbar_visible(toolbar_visible)

    def get_toolbar_visible(self):
        return self._toolbar_visible

    def set_toolbar_visible(self, visible):
        if visible:
            self._figure.canvas.toolbar.pack(side=BOTTOM, fill=X)
        else:
            self._figure.canvas.toolbar.pack_forget()

        self._toolbar_visible = visible

    def toggle_toolbar(self):
        self.set_toolbar_visible(not self._toolbar_visible)

    def get_figure(self):
        return self._figure
