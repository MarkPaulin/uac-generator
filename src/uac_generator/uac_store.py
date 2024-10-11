from pathlib import Path


class UacExistsError(Exception):
    pass


class UacStore:
    def __init__(self):
        self.uacs = set()

    def add(self, uac: str) -> None:
        if self.uac_exists(uac):
            raise UacExistsError
        self.uacs.add(uac)

    def uac_exists(self, uac: str) -> bool:
        return uac in self.uacs


class FileUacStore(UacStore):
    def __init__(self, file: Path):
        self.file = Path(file).expanduser()
        if self.file.exists():
            with open(self.file, "r") as f:
                self.uacs = set(line.rstrip() for line in f)
        else:
            self.uacs = set()
            self.file.touch()

    def add(self, uac: str):
        if self.uac_exists(uac):
            raise UacExistsError
        self.uacs.add(uac)
        with open(self.file, "a") as f:
            f.write(uac + "\n")
