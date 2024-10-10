import random


class UacExistsError(Exception):
    pass


class UacGenerator:
    def __init__(self, character_set, length, max_attempts):
        self.character_set = [str(c) for c in set(character_set)]
        self.length = length
        self.max_attempts = max_attempts
        self.uacs = set()

    def store_uac(self, uac):
        if uac in self.uacs:
            raise UacExistsError
        else:
            self.uacs.add(uac)

    def generate_uac(self):
        uac = "".join(
            [
                self.character_set[random.randrange(len(self.character_set))]
                for i in range(self.length)
            ]
        )
        self.store_uac(uac)
        return uac

    def new_uac(self, attempt=0):
        if attempt > self.max_attempts:
            raise ValueError(f"Unable to generate UAC in {self.max_attempts} attempts")
        try:
            return self.generate_uac()
        except UacExistsError:
            return self.new_uac(attempt + 1)
