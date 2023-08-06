import colorsys
import random

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import Normalize
import numpy as np


def list_colormaps():
    """List the colormaps available from matplotlib

    Parameters
    ----------

    Returns
    -------
    colormaps : List
        List of the names of the available colormaps
    """
    return plt.colormaps()


def parse_colormap(colormap):
    """Obtains colormap data from the colormap name

    Parameters
    ----------
    colormap : str
        Name of colormap

    Returns
    -------
    cmap: LinearSegmentedColormap
        If colormap is "none" or "None":
            Returns None
        Else:
            Returns colormap data as LinearSegmentedColormap

    """
    if colormap is None:
        _colormap = colormap
    elif type(colormap) == str:
        if colormap.lower() == "none":
            _colormap = None
        elif colormap.lower() == "baker":
            from matplotlib.colors import LinearSegmentedColormap
            import flow_vis

            colorw = flow_vis.make_colorwheel()
            _colormap = LinearSegmentedColormap.from_list('Baker', colorw / 255)
        else:
            assert colormap in plt.colormaps()
            _colormap = plt.cm.get_cmap(colormap)
    else:
        _colormap = colormap

    return _colormap


# color functions
def create_color(use_alpha=False):
    """Generates a random color

    Parameters
    ----------
    use_alpha : bool, optional
        Option to set if the alpha value should be returned

    Returns
    -------
    color : array_like
        If use_alpha is True:
            Returns a 1d array of shape (4,)
        If use_alpha is False:
            Returns a 1d array of shape (3,)

    """
    hue, saturation, luminance = random.random(), 0.5 + random.random() / 2.0, 0.6 + random.random() / 5.0
    red, green, blue = colorsys.hls_to_rgb(hue, saturation, luminance)

    if use_alpha:
        return np.array([red, green, blue, 1])
    else:
        return np.array([[[red, green, blue]]])


def get_colors(inputs, colormap, colormap_min=None, colormap_max=None):
    """Assigns colors to the inputs based on the provided colormap

    Parameters
    ----------
    inputs : array_like
        One dimensional array of values that will be mapped ot the color map
    colormap : LinearSegmentedColormap
        Colormap returned from ``parse_colormap``
    colormap_min : float, optional
        Minimum value used in the scaling of the colormap
    colormap_max : float, optional
        Maximum value used in the scaling of the colormap

    Returns
    -------
    colors : array_like
        Colors assigned to each input based on the colormap provided
    colormap_min : float
        Minimum value used in the scaling of the colormap
    colormap_max : float
        Maximum value used in the scaling of the colormap

    """
    if colormap_min is None and colormap_max is None:
        percentile = np.nanpercentile(inputs, [0.1, 99.9])
        max_value = round(np.max(np.abs(percentile)), 2)
        norm = matplotlib.colors.TwoSlopeNorm(0, -max_value, max_value)
        colormap_min = -max_value
        colormap_max = max_value
    else:
        if colormap_min is None:
            colormap_min = np.min(inputs)
        if colormap_max is None:
            colormap_max = np.max(inputs)
        norm = matplotlib.colors.Normalize(colormap_min, colormap_max)
    return colormap(norm(inputs)), colormap_min, colormap_max


def save_colorwheel(colormap,
                    filepath=None,
                    figsize=(8, 8)):
    """Output colormap as a color wheel

    Parameters
    ----------
    colormap : str or LinearSegmentedColormap
        Colormap to plot color wheel
    filepath : str, optional
        File path to save color wheel
    figsize : sequence of int of length 2, optional
        Size of output figure

    Returns
    -------
    colorwheel : ndarray
        Ndarray of the color wheel image

    """
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # See: https://stackoverflow.com/questions/31940285/plot-a-polar-color-wheel-based-on-a-colormap-using-python-matplotlib
        # Generate a figure with a polar projection
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar')

        # Define colormap normalization for 0 to 2*pi
        norm = Normalize(0, 2*np.pi)

        # Plot a color mesh on the polar plot
        # with the color set by the angle
        n = 500  # the number of secants for the mesh
        t = np.linspace(0, 2*np.pi, n)  # theta values
        r = np.linspace(.8, 1, 2)  # radius values change 0.6 to 0 for full circle
        rg, tg = np.meshgrid(r, t)  # create a r,theta meshgrid
        c = tg  # define color values as theta value
        ax.pcolormesh(t, r, c.T, shading='auto', norm=norm,
                      cmap=colormap)  # plot the colormesh on axis with colormap
        ax.set_yticklabels([])  # turn of radial tick labels (yticks)
        ax.tick_params(pad=20, labelsize=24)  # cosmetic changes to tick labels
        ax.spines['polar'].set_visible(False)  # turn off the axis spine.

        if filepath is not None:
            fig.savefig(filepath, dpi=200)

        fig.canvas.draw()
        buf = fig.canvas.buffer_rgba()
        colorwheel = np.asarray(buf, dtype=np.uint8)[..., :3]
        colorwheel = colorwheel[np.newaxis, ...]  # to facilitate loading into the imageviewer widget
        plt.close(fig)

        return colorwheel


def save_colorbar(colormap, filepath=None, figsize=(6, 1), colormap_min=-1, colormap_max=1, orientation='horizontal'):
    """Output colormap as a color bar

    Parameters
    ----------
    colormap : str or LinearSegmentedColormap
        Colormap to plot color wheel
    filepath : str, optional
        File path to save color wheel
    figsize : sequence of int of length 2, optional
        Size of output figure
    colormap_min : float, optional
        Minimum value used in the scaling of the colormap
    colormap_max : float, optional
        Maximum value used in the scaling of the colormap
    orientation : str, optional
        Determines if the color bar should be plotted in the horizontal or vertical orientation

    Returns
    -------
    colorbar : ndarray
        Ndarray of the color bar image

    """
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        fig, ax = plt.subplots(figsize=figsize)
        fig.subplots_adjust(bottom=0.5)

        norm = matplotlib.colors.Normalize(vmin=colormap_min, vmax=colormap_max)

        fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=colormap),
                     cax=ax, orientation=orientation)
        plt.xticks(fontsize=18)
        plt.tight_layout()

        if filepath is not None:
            fig.savefig(filepath, dpi=200)

        fig.canvas.draw()
        buf = fig.canvas.buffer_rgba()
        colorbar = np.asarray(buf, dtype=np.uint8)[..., :3]
        colorbar = colorbar[np.newaxis, ...]  # to facilitate loading into the imageviewer widget
        plt.close(fig)

        return colorbar
