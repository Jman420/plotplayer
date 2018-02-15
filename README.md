# plotplayer
Lightweight function based animation player for Matplotlib

# Description
This is a complete re-write of bilylee's videofig project (https://github.com/bilylee/videofig) with
a focus on Object Oriented Principles, as well as some additional features for convenience.

# Features
- Support pre-created Matplotlib Figure and Axis as animation canvas
- Support multiple semi-independent simultaneous playbacks (see Usage section below)
- Support scrubbing via Slider and Keyboard Shortcuts during playback
- Support saving animation as video, html and javascript
- Support hiding/showing Matplotlib Toolbar
- Support custom Key Press Handler
- Support overriding Keyboard Shortcuts
- Support custom Skip and Jump Sizes
- Support custom initial window size (set via aspect ratio: (4,3); default:(8,4.5); (16,9); (21,9), etc)
- Pip scripts for easy installation

# Keyboard Shortcuts
* Toggle Toolbar - T
* Toggle Playback - Space/Enter
* Skip Ahead - Right
* Skip Back - Left
* Jump Ahead - Up
* Jump Back - Down
* Jump to Beginning - Home
* Jump to End - End

# Saving as Video
To save an animation as a video press and hold the 's' key and then press one of the following keys
to select the output format:
* V - mp4 video using ffmpeg (must have ffmpeg installed)
* H - HTML5 video
* J - Javascript video

# Installation
plotplayer includes pip scripts to handle installation into the Python Environment.  First clone the
plotplayer repository and then run the following command:

```
pip install <path to plotplayer repo root>
```

# Usage
# Basic Usage
```python
player = plotplayer("Dummy Animation")
player.initializeAnimation(100, drawFunc)
plotplayer.showPlayers()
```
This will display a plotplayer window associated with 100 frames of animation drawn by the drawFunc()
method.  The player will wait for user input to begin playback.  A call to the plotplayer.showPlayers()
method is required as the final line for playback to begin.  The parameter to the
plotplayer.showPlayers() method must be True, if provided.  To display plotplayer windows and continue
executing code after the plotplayer.showPlayers() method call you can provide False as the parameter,
but playback and input handled by plotplay will not function until a blocking call is made to
plotplayer.showPlayers() either with no parameters or the parameter True.

## Automatic Playback
```python
player = plotplayer("Dummy Animation")
player.initializeAnimation(100, drawFunc)
player.play()
plotplayer.showPlayers()
```
This will auto playback 100 frames of animation drawn by the drawFunc() method.

## Multiple Simultaneous Playbacks
```python
player1 = plotplayer("Dummy Animation 1")
player1.initializeAnimation(50, drawFunc)

player2 = plotplayer("Dummy Animation 2")
player2.initializeAnimation(100, drawFunc)

player1.play()
player2.play()

plotplayer.showPlayers()
```
When displaying multiple simultaneous playbacks if an error is encountered all playback windows
will be closed due to unexpected behavior.  It is highly recommended to stop playback before
closing any of the playback windows to avoid these types of errors.

## Pre-Created Figure
```python
figure = matplotlib.pylab.plt.figure()
player = plotplayer("Dummy Animation", figure)
player.initializeAnimation(100, drawFunc)
plotplayer.showPlayers()
```
The pre-created figure must be of type matplotlib.figure.Figure.  If no axes are present on the
figure then one will be added as the animation canvas.  If axes exist then the current axes is
treated as the animation canvas.  An axis will always be added for the slider at the bottom of
the window.

## Custom Key Press Handler
```python
def keyPressHandler(eventData):
    print(eventData)
    return False

player = plotplayer("Dummy Animation", keyPressHandler=keyPressHandler)
player.initializeAnimation(100, drawFunc)
plotplayer.showPlayers()
```
A Custom Key Press Handler can override Default Keyboard Shortcuts by returning True.  This
indicates to plotplayer that the key press has been handled and to stop processing the event.

# Examples
See [plotplayer_test.py](plotplayer/plotplayer_test.py)