from subversion_rando.terrain_patch_data import (
    wrecked_air_lock, wrecked_air_lock_screw_bts, wrecked_air_lock_screw_layer_1
)


def test() -> None:
    for i in wrecked_air_lock_screw_layer_1:
        assert wrecked_air_lock[i: i + 2] == b'\xbf\xb0'
        print(wrecked_air_lock[i: i + 2])
    bts_value = 9
    for i in wrecked_air_lock_screw_bts:
        assert wrecked_air_lock[i] == bts_value
        bts_value += 1
        print(wrecked_air_lock[i])


if __name__ == "__main__":
    test()
