"""
Root PlotPlayer Package contains all the data structures, modules and classes used by the
PlotPlayer project.

Public Modules:
  * plotplayer - Contains the PlotPlayer interface and functionality; this is the most
      common entry point for most usages

Subpackages:
  * helpers - Contains various modules containing miscellaneous helper methods
  * managers - Contains modules related to managing the plotplayer functionality
  * validators - Contains modules related to input and type validation
"""

# Prevent usage of backends other than Tkinter
import matplotlib


matplotlib.use("TkAgg")
