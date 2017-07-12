import numpy.testing as npt

import radiant


def test_plane():
    plane = radiant.PlaneGeometry()
    npt.assert_array_equal(plane.index, [[0, 2, 1], [2, 3, 1]])
