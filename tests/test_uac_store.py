import pytest

from uac_generator.uac_store import FileUacStore, UacExistsError, UacStore


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


def test_file_uac_store_stores_uacs(tmpdir):
    file = tmpdir / "uacs.txt"
    store = FileUacStore(file)
    assert file.exists()
    uacs = ["aaa", "bbb", "ccc"]
    for uac in uacs:
        store.add(uac)
    assert store.uacs == set(uacs)
    assert all(store.uac_exists(uac) for uac in uacs)
    store.save()
    new_store = FileUacStore(file)
    assert all(new_store.uac_exists(uac) for uac in uacs)
    with pytest.raises(UacExistsError):
        new_store.add("aaa")
    with open(file) as f:
        lines = [line.rstrip() for line in f]
    assert len(lines) == len(uacs)
    assert set(lines) == set(uacs)
