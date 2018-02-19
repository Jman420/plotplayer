WRITE_FILE_MODE = 'w'

def saveVideo(plotPlayer, fileName, writer=None):
    plotPlayer._animation.save(fileName, writer)

def saveFile(fileName, data):
    file = open(fileName, WRITE_FILE_MODE)
    file.write(data)
    file.close()