import csv
from pathlib import Path


class UacExistsError(Exception):
    pass


class UacStore:
    def __init__(self):
        self.uacs = set()
        self.case_info = list()

    def add(self, uac: str, case_info: list = None) -> None:
        if self.uac_exists(uac):
            raise UacExistsError
        self.uacs.add(uac)
        new_case = [uac, *case_info] if case_info else [uac]
        self.case_info.append(new_case)

    def uac_exists(self, uac: str) -> bool:
        return uac in self.uacs


class FileUacStore(UacStore):
    def __init__(self, file: Path):
        self.file = Path(file).expanduser()
        if self.file.exists():
            with open(self.file, "r") as f:
                self.case_info = [row for row in csv.reader(f)]
                self.uacs = set(row[0] for row in self.case_info)
        else:
            self.uacs = set()
            self.case_info = list()
            self.file.touch()

    def add(self, uac: str, case_info: list = None):
        if self.uac_exists(uac):
            raise UacExistsError
        self.uacs.add(uac)
        with open(self.file, "a") as f:
            new_row = [uac, *case_info] if case_info else [uac]
            filewriter = csv.writer(f)
            filewriter.writerow(new_row)
