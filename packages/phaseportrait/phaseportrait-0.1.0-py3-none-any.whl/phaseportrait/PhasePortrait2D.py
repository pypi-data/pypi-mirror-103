from inspect import signature

from .exceptions import *
from . import sliders
from .utils import utils

import matplotlib
import matplotlib.pyplot as plt

import numpy as np

class PhasePortrait2D:
    """
    Makes a phase portrait of a 2D system.
    """
    _name_ = 'PhasePortrait2D'
    def __init__(self, dF, Range, *, MeshDim=10, dF_args={}, Density = 1, Polar = False, Title = 'Phase Portrait', xlabel = 'X', ylabel = r"$\dot{X}$", color='rainbow'):

        
        self.dF_args = dF_args                           # dF function's args
        self.dF = dF                                     # Function containing system's equations
        self.Range = Range                               # Range of graphical representation
        
        
        self.L = int (MeshDim*abs(self.Range[0,0]-self.Range[0,1]))      # Number of points in the meshgrid
        self.Density = Density                                           # Controls concentration of nearby trajectories
        self.Polar = Polar                                               # If dF expression given in polar coord. mark as True
        self.Title = Title                                               # Title of the plot
        self.xlabel = xlabel                                             # Title on X axis
        self.ylabel = ylabel                                             # Title on Y axis


        # Variables for plotting
        self.fig, self.ax = plt.subplots()
        self.color = color
        self.sliders = {}

        # Meshgrid 
        self._X, self._Y = np.meshgrid(np.linspace(*self.Range[0,:], self.L), np.linspace(*self.Range[1,:], self.L))

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Cartesian representation to polar representation transform


    def plot(self, *, color=None):
        self._draw_streamplot(color=color if color else self.color)

        self.fig.canvas.draw_idle()


    def _draw_streamplot(self, *, color=None):

        self.dF_args = {name: slider.value for name, slider in self.sliders.items() if slider.value!= None}

        if self.Polar:
            self._PolarTransformation()
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
        colors = (self._dX**2+self._dY**2)**(0.5)
        colors_norm = matplotlib.colors.Normalize(vmin=colors.min(), vmax=colors.max())
        stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colors, cmap=color, norm=colors_norm, linewidth=1, density= self.Density)
        self.ax.set_xlim(self.Range[0,:])
        self.ax.set_ylim(self.Range[1,:])
        x0,x1 = self.ax.get_xlim()
        y0,y1 = self.ax.get_ylim()
        self.ax.set_aspect(abs(x1-x0)/abs(y1-y0))
        self.ax.set_title(f'{self.Title}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.grid()
        
        return stream


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a slider on an existing plot
        """
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    
    def _PolarTransformation(self):
        """
        Computes the expression of the velocity field if coordinates are given in polar representation
        """
        self._dR, self._dTheta = self.dF(self._R, self._Theta, **self.dF_args)
        self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta



    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        sig = signature(func)
        if len(sig.parameters)<2 + len(self.dF_args):
            raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def Range(self):
        return self._Range


    @Range.setter
    def Range(self, value):
        self._Range = np.array(utils.construct_interval(value, dim=2))

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value
