import numpy as np
import numpy.testing as npt
import pyrr
import pytest

import radiant


def test_immutability():
    a = radiant.Object3D()

    # should all be readonly
    with pytest.raises(ValueError):
        a.rotation[0] = 5
        a.scale[0] = 5
        a.scale.x = 5
        a.position[1] = 5
        a.position.y = 5
        a.children = [5]


def test_model_matrix():
    a = radiant.Object3D()

    assert a.dirty is True
    a.update()
    assert a.dirty is False

    a.rotation = pyrr.Quaternion.from_y_rotation(np.pi)
    a.position = [10, 0, -5]
    a.scale = [1, 1, 2]
    assert a.dirty is True
    a.update()
    assert a.dirty is False

    expected = np.array([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -2, 0],
        [10, 0, -5, 1],
    ], dtype='f4')
    npt.assert_almost_equal(a.model, expected)
    assert a.model.dtype == expected.dtype


def test_rotation():
    a = radiant.Object3D()
    assert a.dirty is True
    a.update()
    assert a.dirty is False

    values = [
        pyrr.Quaternion.from_x_rotation(0),
        pyrr.Matrix33.from_x_rotation(0),
        pyrr.Matrix44.from_x_rotation(0),
        [0, 0, 0],
        np.array([0, 0, 0]),
        np.identity(4),
        np.identity(3),
    ]
    a_id = id(a.rotation)
    for value in values:
        a.rotation = value
        assert id(a.rotation) != a_id
        a_id = id(a.rotation)
        assert a.dirty is True
        a.update()
        assert a.dirty is False
        npt.assert_array_equal(a.rotation, [0.,  0.,  0.,  1.])
        assert a.rotation.dtype.kind == 'f'
        assert a.rotation.dtype.itemsize == 4
        assert isinstance(a.rotation, pyrr.Quaternion)
