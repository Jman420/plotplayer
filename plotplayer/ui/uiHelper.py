from tkinter import filedialog
import matplotlib.pylab as pylab

def getSaveDialogResult(title, defaultFileName, fileTypes=[ ALL_FILES_TYPE ], defaultExtension=ALL_FILES_EXTENSION):
    saveFileName = filedialog.asksaveasfilename(title=title, filetypes=fileTypes,
                                               defaultextension=defaultExtension, initialfile=defaultFileName)
    return saveFileName

def showPlayers(blocking=True):
    try:
        pylab.plt.show(blocking)
    except AttributeError:
        print('Videofig encountered a playback error.')
        print('This is usually due to a videofig window getting closed during animation playback...')
        print('This causes all open videofig windows to malfunction.')
        print('Closing all videofig windows...')
        pylab.plt.close('all')
        pass