"""Prevent usage of Matplotlib backends other than Tkinter"""

import matplotlib


matplotlib.use("TkAgg")
