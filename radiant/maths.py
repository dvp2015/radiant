import numpy as np
import pyrr


__all__ = ('decompose',)


def decompose(matrix44):
    # indexing pyrr matrices is not a pleasant experience, so let's
    matrix44 = np.asarray(matrix44)

    scale = np.linalg.norm(matrix44[:3, :3], axis=0)

    det = np.linalg.det(matrix44)
    if det < 0:
        scale[0] *= -1

    position = matrix44[3, :3]

    rotation = matrix44[:3, :3] * (1 / scale)

    return pyrr.Vector3(scale), pyrr.Quaternion.from_matrix(rotation), pyrr.Vector3(position)
