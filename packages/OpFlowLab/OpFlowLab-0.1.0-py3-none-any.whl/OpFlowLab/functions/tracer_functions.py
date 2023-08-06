import cv2
import numpy as np
from numba import njit, prange


def draw_tracer(image, centroids, color):
    """
    Draws tracers at the specified locations

    Parameters
    ----------
    image : array
        Image on which the tracers are drawn
    centroids : array
        Array containing the positions of tracers
    color : array
        Array containing the color information for each tracer

    Returns
    -------
    image : array
        Image containing the drawn tracers
    """
    tracer_x = centroids[:, 1]
    tracer_y = centroids[:, 0]

    for i, (x, y) in enumerate(zip(tracer_x, tracer_y), 1):
        image = cv2.circle(image, (x, y), 3, color[i - 1][0][0], -1)

    return image


@njit(parallel=True)
def update_tracer(centroids, flow_y, flow_x):
    """
    Updates the position of the tracers using the velocity field

    Parameters
    ----------
    centroids : array
        Array containing the positions of tracers
    flow_x, flow_y : array
        Arrays containing the x and y components of the velocity field respectively

    Returns
    -------
    output : array
        Array containing the updated position of the tracers
    """
    tracer_y = centroids[:, 0].copy()
    tracer_x = centroids[:, 1].copy()

    for i in prange(tracer_x.shape[0]):
        if tracer_x[i] == np.nan or tracer_y[i] == np.nan:
            continue
        else:
            x = np.int(tracer_x[i])
            y = np.int(tracer_y[i])
            if 0 < x < flow_x.shape[1] - 1 and \
                    0 < y < flow_x.shape[0] - 1:
                tracer_x[i] = tracer_x[i] + flow_x[y, x]
                tracer_y[i] = tracer_y[i] + flow_y[y, x]

                if tracer_x[i] > flow_x.shape[1] - 1 or \
                        tracer_x[i] < 0 or \
                        tracer_y[i] > flow_x.shape[0] - 1 or \
                        tracer_y[i] < 0:
                    tracer_x[i] = np.nan
                    tracer_y[i] = np.nan

    output = np.vstack((tracer_y, tracer_x)).T

    return output