import numpy as np
import pyrr


__all__ = ('decompose',)


def decompose(m):
    # indexing pyrr matrices is not a pleasant experience, so let's
    m = np.asarray(m)

    scale = np.linalg.norm(m[:3, :3], axis=1)

    det = np.linalg.det(m)
    if det < 0:
        scale[0] *= -1

    position = m[3, :3]

    rotation = m[:3, :3] * (1 / scale)[:, None]

    return pyrr.Vector3(scale), pyrr.Quaternion.from_matrix(rotation), pyrr.Vector3(position)
