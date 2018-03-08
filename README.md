# plotplayer
Function based animation player for Matplotlib

# Dependencies
  * Python v3.6.3
  * Matplotlib (https://matplotlib.org/)

# Description
This is a complete re-write of bilylee's videofig project (https://github.com/bilylee/videofig) with
a focus on Object Oriented Principles, as well as some additional features for convenience.

# Features
- Support pre-created Matplotlib Figure and Axes as animation canvas
- Support multiple semi-independent simultaneous playbacks (see Usage section below)
- Support scrubbing via Slider and Keyboard Shortcuts during playback
- Support saving animation as video, html and javascript
- Support hiding/showing Matplotlib Toolbar
- Support custom Key Press, Release and Mouse Button Press Handlers
- Support overriding Keyboard Shortcuts
- Support custom Skip and Jump Sizes
- Support custom initial window size (set via aspect ratio: (4,3); default:(8,4.5); (16,9); (21,9), etc)
- Pip scripts for easy installation

# Keyboard Shortcuts
* Toggle Slider - T
* Toggle Toolbar - M
* Toggle Playback - Space/Enter
* Skip Ahead - Right
* Skip Back - Left
* Jump Ahead - Up
* Jump Back - Down
* Jump to Beginning - Home
* Jump to End - End
* Save Video - D + File Selection Key (see below)

# Saving as Video
To save an animation as a video press and hold the 'D' key and then press one of the following keys
to select the output format:
* V - mp4 video using ffmpeg (must have ffmpeg installed)
* H - HTML5 video
* J - Javascript video

A save file dialog will appear to prompt you for the name of the file to save.  (Note : allow a few
seconds for the dialog to load)

# Matplotlib Interactive Navigation Controls
See https://matplotlib.org/users/navigation_toolbar.html for details including Matplotlib keyboard
shortcuts.

# Installation
plotplayer includes pip scripts to handle installation into the Python Environment.  First clone the
plotplayer repository and then run the following command:

```
pip install <path to plotplayer repo root>
```

# Usage
# Basic Usage
```python
player = PlotPlayer()
player.initialize(100, drawFunc)
PlotPlayer.show_players()
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
player = PlotPlayer()
player.initialize(100, drawFunc)
player.play()
PlotPlayer.show_players()
```
This will auto playback 100 frames of animation drawn by the drawFunc() method.

## Multiple Simultaneous Playbacks
```python
player1 = PlotPlayer()
player1.initialize(50, drawFunc)

player2 = PlotPlayer()
player2.initialize(100, drawFunc)

player1.play()
player2.play()

PlotPlayer.show_players()
```
When displaying multiple simultaneous playbacks if an error is encountered all playback windows
will be closed due to unexpected behavior.  It is highly recommended to stop playback before
closing any of the playback windows to avoid these types of errors.

## Pre-Created Figure
```python
figure = matplotlib.pyplot.figure()
window_handler = WindowManager(figure)
player = PlotPlayer(window_handler)
player.initialize(100, drawFunc)
PlotPlayer.show_players()
```
The pre-created figure must be of type matplotlib.figure.Figure.  If no axes are present on the
figure then one will be added as the animation canvas.  If axes exist then the current axes is
treated as the animation canvas.  An axis will always be added for the slider at the bottom of
the window.

## Custom Key Press Handler
```python
def key_press_handler(eventData):
    print(eventData)
    return False

player = PlotPlayer("Dummy Animation")
input_handler = player.get_input_manager()
input_handler.add_key_press_handler(key_press_handler)
player.initialize(100, drawFunc)
PlotPlayer.show_players()
```
A Custom Key Press Handler can override Default Keyboard Shortcuts by returning True.  This
indicates to plotplayer that the key press has been handled and to stop processing the event.
These same patterns are applied to Custom Key Release and Mouse Button Press Handlers as well.

# Examples
See [plotplayer_test.py](plotplayer/plotplayer_test.py)

Also the fractimation project uses plotplayer : https://github.com/Jman420/fractimation