import random

from uac_generator.uac_store import UacExistsError, UacStore


class UacGenerator:
    def __init__(
        self, store: UacStore, character_set: list, length: int, max_attempts: int = 5
    ):
        self.character_set = [str(c) for c in set(character_set)]
        self.length = length
        self.max_attempts = max_attempts
        self.store = store

    def store_uac(self, uac: str, case_info: list = None) -> None:
        self.store.add(uac, case_info)

    def generate_uac(self, case_info: list = None) -> str:
        uac = "".join(
            [
                self.character_set[random.randrange(len(self.character_set))]
                for i in range(self.length)
            ]
        )
        self.store_uac(uac, case_info)
        return uac

    def new_uac(self, case_info: list = None, attempt: int = 0) -> str:
        if attempt > self.max_attempts:
            raise ValueError(f"Unable to generate UAC in {self.max_attempts} attempts")
        try:
            return self.generate_uac(case_info)
        except UacExistsError:
            return self.new_uac(case_info, attempt + 1)
