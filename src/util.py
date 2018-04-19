import queue
import numpy as np


def get_all_from_queue(q):
    """
    Returns at least one element from the queue, tries to return as many as possible.
    :param q: The queue to get elements from
    :return: A list of elements fetched from the queue
    """
    data = [q.get()]
    while True:
        try:
            data.append(q.get_nowait())
        except queue.Empty:
            return data


def triangle_patch(centroid, rot, side):
    """
    Compute the coordinates of a triangle
    :param centroid: Triangle centroid coordinates
    :param rot: Triangle rotation
    :param side: Length of side
    :return: A 3 by 2 array representing the coordinates of a triangle
    """
    height = np.sqrt(3) / 2 * side
    relative_coords = np.array([[-height / 3, -side / 2], [-height / 3, side / 2], [2 * height / 3, 0]])
    s, c = np.sin(rot), np.cos(rot)
    rotated = relative_coords @ np.array([[c, s], [-s, c]])
    coords = np.array([centroid]) + rotated
    return coords


def scaled_coords(coords, width, height):
    """
    Returns coordinates scaled and translated to fit within a viewport with no deformation
    :param coords: An n-by-2 array of coordinates
    :return: An n-by-2 array of coordinates
    """
    xlim = np.min(coords[:, :, 0]), np.max(coords[:, :, 0])
    ylim = np.min(coords[:, :, 1]), np.max(coords[:, :, 1])

    scale = min(width / (xlim[1] - xlim[0]), height / (ylim[1] - ylim[0]))
    print(scale)

    ret = coords.copy()

    ret[:, :, 0] -= xlim[0]
    ret[:, :, 1] -= ylim[0]
    return ret * scale
