import numpy as np
import numpy.testing as npt
import pyrr

from radiant import maths


def test_decompose():
    # define expectations
    expected_scale = pyrr.Vector3([1, 1, 2], dtype='f4')
    expected_rotation = pyrr.Quaternion.from_y_rotation(np.pi, dtype='f4')
    expected_translation = pyrr.Vector3([10, 0, -5], dtype='f4')
    expected_model = pyrr.Matrix44([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -2, 0],
        [10, 0, -5, 1],
    ], dtype='f4')

    # compose matrix using Pyrr
    s = pyrr.Matrix44.from_scale(expected_scale, dtype='f4')
    r = pyrr.Matrix44.from_quaternion(expected_rotation, dtype='f4')
    t = pyrr.Matrix44.from_translation(expected_translation, dtype='f4')
    model = t * r * s
    npt.assert_almost_equal(model, expected_model)
    assert model.dtype == expected_model.dtype

    # decompose matrix
    scale, rotation, translation = maths.decompose(model)
    npt.assert_almost_equal(scale, expected_scale)
    assert scale.dtype == expected_scale.dtype
    npt.assert_almost_equal(rotation, expected_rotation)
    assert rotation.dtype == expected_rotation.dtype
    npt.assert_almost_equal(translation, expected_translation)
    assert translation.dtype == expected_translation.dtype
