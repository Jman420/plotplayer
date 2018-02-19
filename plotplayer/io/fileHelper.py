WRITE_FILE_MODE = 'w'

def saveVideo(animation, fileName, writer=None):
    animation.save(fileName, writer)

def saveFile(fileName, data):
    file = open(fileName, WRITE_FILE_MODE)
    file.write(data)
    file.close()