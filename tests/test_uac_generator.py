from uac_generator.uac_generator import UacGenerator
from uac_generator.uac_store import UacStore


def test_uac_generator_generates_uacs():
    store = UacStore()
    character_set = range(0, 10)
    length = 5
    max_attempts = 2
    generator = UacGenerator(
        character_set=character_set,
        length=length,
        max_attempts=max_attempts,
        store=store,
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
