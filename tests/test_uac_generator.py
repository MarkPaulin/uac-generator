import pytest

from uac_generator.uac_generator import UacGenerator
from uac_generator.uac_store import FileUacStore, UacStore


def test_uac_generator_generates_uacs():
    store = UacStore()
    character_set = range(0, 10)
    length = 5
    max_attempts = 2
    generator = UacGenerator(
        store=store,
        character_set=character_set,
        length=length,
        max_attempts=max_attempts,
    )

    uac = generator.new_uac()
    assert len(uac) == length
    assert all(c in map(str, character_set) for c in uac)
    assert store.uac_exists(uac)
    try:
        uac2 = generator.new_uac()
        assert uac != uac2
    except ValueError:
        pass


def test_uac_generator_can_use_file_store(tmpdir):
    file = tmpdir / "uacs.txt"
    store = FileUacStore(file)
    character_set = range(0, 10)
    length = 5
    max_attempts = 2
    generator = UacGenerator(
        store=store,
        character_set=character_set,
        length=length,
        max_attempts=max_attempts,
    )

    uacs = [generator.new_uac() for i in range(5)]
    with open(file) as f:
        lines = [line.rstrip() for line in f]
    assert len(lines) == 5
    assert set(lines) == set(uacs)


def test_uac_generator_throws_error():
    store = UacStore()
    character_set = range(0, 10)
    length = 1
    max_attempts = 0
    generator = UacGenerator(
        store=store,
        character_set=character_set,
        length=length,
        max_attempts=max_attempts,
    )

    with pytest.raises(ValueError):
        [generator.new_uac() for i in range(11)]
