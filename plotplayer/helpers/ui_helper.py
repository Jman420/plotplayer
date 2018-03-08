"""
Miscellaneous UI helper methods
"""

from tkinter.filedialog import asksaveasfilename
from matplotlib import pyplot

ALL_FILES_EXTENSION = '*.*'
ALL_FILES_TYPE = ['All Files', ALL_FILES_EXTENSION]

def get_save_dialog_result(title, default_file_name, file_types=None,
                           default_extension=ALL_FILES_EXTENSION):
    """
    Displays a Save File Dialog and returns the resulting file name
    """
    if file_types is None:
        file_types = [ALL_FILES_TYPE]

    save_file_name = asksaveasfilename(title=title, filetypes=file_types,
                                       defaultextension=default_extension,
                                       initialfile=default_file_name)
    return save_file_name

def show_players(blocking=True):
    """
    Shows all Pyplot figures.  Wraps the call in a try-catch block to avoid crashes.
    """
    try:
        pyplot.show(blocking)
    except AttributeError:
        print('Plotplayer encountered a playback error.')
        print('This is usually due to a plotplayer window getting closed ' +
              'during animation playback...')
        print('This causes all open plotplayer windows to malfunction.')
        print('Closing all plotplayer windows...')
        pyplot.close('all')
