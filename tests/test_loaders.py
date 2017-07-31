import radiant


def test_plane_obj():
    with open("examples/resources/plane.obj", mode="r") as fh:
        geometry = radiant.load_obj(fh)

    assert geometry.attributes['pos'].shape == (6, 3)
    assert geometry.attributes['pos'].dtype.kind == 'f'
    assert geometry.attributes['pos'].dtype.itemsize == 4
    assert geometry.attributes['uv'].shape == (6, 2)
    assert geometry.attributes['uv'].dtype.kind == 'f'
    assert geometry.attributes['uv'].dtype.itemsize == 4
    assert geometry.attributes['normal'].shape == (6, 3)
    assert geometry.attributes['normal'].dtype.kind == 'f'
    assert geometry.attributes['normal'].dtype.itemsize == 4
    assert geometry.index is None


def test_dragon_obj():
    with open("examples/resources/dragon.obj", mode="r") as fh:
        geometry = radiant.load_obj(fh)

    assert geometry.attributes['pos'].shape == (45882, 3)
    assert geometry.attributes['pos'].dtype.kind == 'f'
    assert geometry.attributes['pos'].dtype.itemsize == 4
    assert geometry.attributes['uv'].shape == (45882, 2)
    assert geometry.attributes['uv'].dtype.kind == 'f'
    assert geometry.attributes['uv'].dtype.itemsize == 4
    assert geometry.attributes['normal'].shape == (45882, 3)
    assert geometry.attributes['normal'].dtype.kind == 'f'
    assert geometry.attributes['normal'].dtype.itemsize == 4
    assert geometry.index is None
