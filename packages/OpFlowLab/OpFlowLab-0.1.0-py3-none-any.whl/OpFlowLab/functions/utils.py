import glob
import os

import scipy.signal
import skimage.io
from scipy.io import loadmat

from .interpolation import *


def imadjust(image, in_bound=(0.001, 0.999), out_bound=(0, 1)):
    """Performs contrast adjustment on an image

    Parameters
    ----------
    image : ndarray
        Input image.
    in_bound : tuple
        Tuple specifying the lower and upper percentile with which to set the input contrast limit.
    out_bound : tuple
        Tuple specifying the lower and upper percentile with which to set the output contrast limit.

    Returns
    -------
    output : ndarray
        Contrast adjusted output image.

    Notes
    -----
    See https://stackoverflow.com/questions/39767612/what-is-the-equivalent-of-matlabs-imadjust-in-python/44529776#44529776

    """

    assert len(image.shape) == 2, 'Input image should be 2-dims'
    image_dtype = image.dtype

    if image_dtype == 'uint8':
        range_value = 255
    elif image_dtype == 'uint16':
        range_value = 65535
    else:
        range_value = 1

    # Compute in and out limits
    in_bound = np.percentile(image, np.multiply(in_bound, 100))
    out_bound = np.multiply(out_bound, range_value)

    # Stretching
    scale = (out_bound[1] - out_bound[0]) / (in_bound[1] - in_bound[0])

    image = image - in_bound[0]
    image[image < 0] = 0

    output = image * scale + out_bound[0]
    output[output > out_bound[1]] = out_bound[1]

    output = output.astype(image_dtype)

    return output


def load_velocity_filelist(folder,
                           velocity_type='dense', xy_folder_list=('flowx', 'flowy'), file_ext='*.bin',
                           reverse_sort=False):
    """Returns the list of files containing the velocity fields.

    Parameters
    ----------
    folder : str
        Input folder
    velocity_type : {‘dense’, ‘sparse’}
        Specifies the type of velocity field.
    xy_folder_list : tuple
        Subfolders to search for the x and y component of the velocity field. Only used when the velocity type is 'dense'.
    file_ext : str
        Regex string specifying the file extension.
    reverse_sort : bool
        Specify if the files should be sorted in the reverse order instead of the forward order.

    Returns
    -------
    list
        If the velocity type is 'dense', returns a list containing two file lists pointing to the x component and y component of the velocity field.
        If the velocity type is 'sparse', returns a list containing a single file list.

    """

    velocity_type = velocity_type.lower()
    if velocity_type == 'dense':
        vector_x_filelist = glob.glob(os.path.join(folder, xy_folder_list[0], file_ext))
        vector_x_filelist.sort(reverse=reverse_sort)
        vector_y_filelist = glob.glob(os.path.join(folder, xy_folder_list[1], file_ext))
        vector_y_filelist.sort(reverse=reverse_sort)
        return [vector_x_filelist, vector_y_filelist]
    elif velocity_type == 'sparse':
        vector_filelist = glob.glob(os.path.join(folder, file_ext))
        vector_filelist.sort(reverse=reverse_sort)
        return [vector_filelist]


def load_velocity_bin(bin_file, shape, bin_dtype="float32", kernel_size=5, replace_nan=True):
    """Returns the list of files containing the velocity fields.

    Parameters
    ----------
    bin_file : str
        Path to the binary file to load.
    shape : tuple
        Tuple containing the dimensions to reshape the binary data to.
    bin_dtype : {"float32", "float16"}
        Dtype that the binary array is encoded with.
    kernel_size : int
        Size of the median filter used.
    replace_nan : bool
        Specifies if NaN values should be replaced with a value of 0

    Returns
    -------
    velocity : array_like
        Array containing the velocities loaded from bin_file

    """

    bin_dtype = bin_dtype.lower()
    if bin_dtype == "float16":
        dtype = np.half
    else:
        dtype = np.float32

    velocity = np.fromfile(bin_file, dtype=dtype)

    # convert back to float32 for future calculations
    if bin_dtype == "float16":
        velocity = np.float32(velocity)

    velocity = np.reshape(velocity, shape)

    if kernel_size is not None:
        velocity = scipy.signal.medfilt2d(velocity, kernel_size=kernel_size)

    if replace_nan == True:
        velocity[np.isnan(velocity)] = 0

    return velocity


def load_velocity_piv(vector_file, frame_no):
    """Loads the velocity field from the output from PIVLab.

    Parameters
    ----------
    vector_file : str
        Path to the MATLAB file to load.
    frame_no : tuple
        Frame number of the velocity field that is to be loaded.

    Returns
    -------
    flow_x : array_like
        Array containing the x component of the velocity field
    flow_y : array_like
        Array containing the y component of the velocity field
    x : array_like
        Array containing the x coordinates of the velocity field
    y : array_like
        Array containing the y coordinates of the velocity field

    """

    piv_mat = loadmat(vector_file)
    x = piv_mat['x'][frame_no][0]
    y = piv_mat['y'][frame_no][0]
    flow_x = piv_mat['u_filtered'][frame_no][0]
    flow_y = piv_mat['v_filtered'][frame_no][0]

    return flow_x, flow_y, x, y


def save_output(array, filename, save_velocity_as_tif=False, save_dtype="float16"):
    """Helper function used to save the velocity field.

    Parameters
    ----------
    array : array_like
        Array to be saved.
    filename : str
        Filename used to save the array.
    save_velocity_as_tif : bool
        Determines if the array should be saved as a tiff or a binary file.
    save_dtype : {"float32", "float16"}
        Specifies if the array should be saved as a float32 array or float 16 array.

    Returns
    -------

    """

    if save_velocity_as_tif:
        skimage.io.imsave('{}.tif'.format(filename), array)
    else:
        if save_dtype == "float16":
            array = array.astype(np.half)

        with open('{}.bin'.format(filename), 'wb') as file:
            array.tofile(file)
        file.close()
