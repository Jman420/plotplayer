# plotplayer
Lightweight function based animation player for Matplotlib

# Description
This is a complete re-write of bilylee's videofig project (https://github.com/bilylee/videofig) with
a focus on Object Oriented Principles, as well as some additional features for convenience.

# Features
- Support pre-created Matplotlib Figure and Axis as animation canvas
- Support multiple semi-independent simultaneous playbacks (see Usage section below)
- Support scrubbing via Slider and Keyboard Shortcuts during playback

# Usage
Basic Playback
```python
player = plotplayer("Dummy Animation")
player.initializeAnimation(100, drawFunc)
player.play()
player.show()
```
This will display 100 frames of animation drawn by the drawFunc() method.  A call to the
plotplayer.show() method is required as the final line for playback to begin.  The parameter to
the plotplayer.show() method must be True, if provided.

Multiple Simultaneous Playbacks
```python
player1 = plotplayer("Dummy Animation 1")
player1.initializeAnimation(50, drawFunc)

player2 = plotplayer("Dummy Animation 2")
player2.initializeAnimation(100, drawFunc)

player1.show(False)
player1.play()

player2.play()
player2.show()
```
All players except the last to be shown must have a call to its show() method with the parameter
False.  This displays the associated plot as non-blocking, allowing for the remaining plots to
show themselves and begin playback.  The final player to be shown must have a call to its show()
with the parameter True, if provided.

When displaying multiple simultaneous playbacks if an error is encountered both playback windows
will be closed due to unexpected behavior.  It is highly recommended to stop playback before
closing any of the playback windows to avoid these types of errors.

Pre-Created Figure
```python
figure = matplotlib.pylab.plt.figure()
player = plotplayer("Dummy Animation", figure)
player.initializeAnimation(100, drawFunc)
player.play()
player.show()
```
The pre-created figure must be of type matplotlib.figure.Figure.  If no axes are present on the
figure then one will be added as the animation canvas.  If axes exist then the current axes is
treated as the animation canvas.  An axis will always be added for the slider at the bottom of
the window.

# Examples
See [plotplayer_test.py]