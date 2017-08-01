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
    with pytest.raises(ValueError):
        a.scale[0] = 5
    with pytest.raises(ValueError):
        a.scale.x = 5
    with pytest.raises(ValueError):
        a.position[1] = 5
    with pytest.raises(ValueError):
        a.position.y = 5
    with pytest.raises(AttributeError):
        a.children = [5]
    with pytest.raises(AttributeError):
        a.children.append(5)


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
        pyrr.Vector3([0, 0, 0]),
        pyrr.Vector4([0, 0, 0, 1]),
        np.array([0, 0, 0]),
        np.array([0, 0, 0, 1]),
        np.identity(4),
        np.identity(3),
        np.array([0, 0, 0]).tolist(),
        np.array([0, 0, 0, 1]).tolist(),
        np.identity(4).tolist(),
        np.identity(3).tolist(),
    ]
    for value in values:
        a.rotation = value
        assert a.dirty is True
        a.update()
        assert a.dirty is False
        npt.assert_array_equal(a.rotation, [0.,  0.,  0.,  1.])
        assert a.rotation.dtype.kind == 'f'
        assert a.rotation.dtype.itemsize == 4
        assert isinstance(a.rotation, pyrr.Quaternion)


def test_model_setter():
    a = radiant.Object3D()
    assert a.dirty is True
    a.update()
    assert a.dirty is False

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

    # call setter
    a.model = expected_model
    assert a.dirty is True
    a.update()
    assert a.dirty is False

    # assertions
    npt.assert_almost_equal(a.scale, expected_scale)
    assert a.scale.dtype == expected_scale.dtype
    npt.assert_almost_equal(a.rotation, expected_rotation)
    assert a.rotation.dtype == expected_rotation.dtype
    npt.assert_almost_equal(a.position, expected_translation)
    assert a.position.dtype == expected_translation.dtype
