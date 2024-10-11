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
