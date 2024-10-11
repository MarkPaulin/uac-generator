import random

from uac_generator.uac_store import UacExistsError, UacStore


class UacGenerator:
    def __init__(
        self, character_set: list, length: int, max_attempts: int, store: UacStore
    ):
        self.character_set = [str(c) for c in set(character_set)]
        self.length = length
        self.max_attempts = max_attempts
        self.store = store

    def store_uac(self, uac: str) -> None:
        self.store.add(uac)

    def generate_uac(self) -> str:
        uac = "".join(
            [
                self.character_set[random.randrange(len(self.character_set))]
                for i in range(self.length)
            ]
        )
        self.store_uac(uac)
        return uac

    def new_uac(self, attempt: int = 0) -> str:
        if attempt > self.max_attempts:
            raise ValueError(f"Unable to generate UAC in {self.max_attempts} attempts")
        try:
            return self.generate_uac()
        except UacExistsError:
            return self.new_uac(attempt + 1)
