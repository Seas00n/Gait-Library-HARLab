import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
from body_idx import *
class FastPlotCanvas(object):
    ax: matplotlib.axes._axes.Axes
    fig: matplotlib.figure.Figure

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.draw()
        self.bd = BodyIdx()
