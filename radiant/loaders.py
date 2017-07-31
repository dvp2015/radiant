import numpy as np

from .geometries import Geometry, Primitives


__all__ = ('load_obj',)


def load_obj(file, **kwargs):
    """
    Parses a Wavefront .obj file.

    Parameters
    ----------
    file : file-like object
        Will be read from line-by-line. Assumed to opened in "r" mode.

    Returns
    -------
    Geometry

    Notes
    -----
    Inefficient implementation; naively duplicates vertex data per face.
    Assumes the format exported by Blender. Does not deal well with missing elements.
    """
    v = []
    vt = []
    vn = []
    f = []
    for line in file:
        if line.startswith("v "):
            v.append([float(x) for x in line[2:].split()])
        elif line.startswith("vt "):
            vt.append([float(x) for x in line[3:].split()])
        elif line.startswith("vn "):
            vn.append([float(x) for x in line[3:].split()])
        elif line.startswith("f "):
            f.append([[int(x) for x in fv.split('/')] for fv in line[2:].split()])

    # now produce the full buffers
    f = np.array(f, dtype='i4')
    f[f > 0] -= 1
    v = np.array(v, dtype='f4')[f[:, :, 0].ravel()]
    vt = np.array(vt, dtype='f4')[f[:, :, 1].ravel()]
    vn = np.array(vn, dtype='f4')[f[:, :, 2].ravel()]

    # NOTE: we could identify unique vertices in f and shave off memory requirements. we could.

    return Geometry({'pos': v, 'uv': vt, 'normal': vn}, primitive=Primitives.TRIANGLES, **kwargs)
