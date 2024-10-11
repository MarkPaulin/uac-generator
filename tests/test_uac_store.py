import pytest

from uac_generator.uac_store import UacExistsError, UacStore


def test_uac_store_stores_uacs():
    store = UacStore()
    uacs = ["aaa", "bbb", "ccc"]
    for uac in uacs:
        store.add(uac)
    assert store.uacs == set(uacs)
    assert all(store.uac_exists(uac) for uac in uacs)


def test_uac_store_throws_error_for_existing_uac():
    store = UacStore()
    uac = "aaa"
    store.add(uac)
    with pytest.raises(UacExistsError):
        store.add(uac)
