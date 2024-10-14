import csv
from pathlib import Path

import pyodbc


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

    def save(self) -> None:
        pass


class FileUacStore(UacStore):
    def __init__(self, file: Path):
        self.new_cases = list()
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
        super().add(uac, case_info)
        self.new_cases.append([uac, *case_info] if case_info else [uac])

    def save(self) -> None:
        with open(self.file, "a", newline="") as f:
            filewriter = csv.writer(f)
            for case in self.new_cases:
                filewriter.writerow(case)
        self.new_cases = []


class SqlUacStore(UacStore):
    def __init__(
        self,
        connection_string: str,
        table_name: str,
        uac_length: int,
        case_info_columns: dict = None,
    ):
        self.connection_string = connection_string
        self.table_name = table_name
        uac_col = {"uac": f"nchar({uac_length}) not null"}
        self.columns = uac_col | case_info_columns if case_info_columns else uac_col
        self.connections = []
        self.check_table_exists()
        self.case_info = self.get_all_case_info()
        self.uacs = set(case[0] for case in self.case_info)
        self.new_cases = list()

    def connect(self):
        if self.connections:
            return self.connections[0]
        else:
            con = pyodbc.connect(self.connection_string)
            self.connections.append(con)
            return con

    def check_table_exists(self):
        con = self.connect()
        cur = con.cursor()
        if not cur.tables(table=self.table_name, tableType="TABLE").fetchone():
            column_statements = ",\n".join(
                f"{key} {value}" for key, value in self.columns.items()
            )
            create_table_query = f"""
                create table {self.table_name} (
                    {column_statements},
                    primary key (uac)
                )
            """
            cur.execute(create_table_query)
            cur.commit()

    def get_all_case_info(self):
        con = self.connect()
        cur = con.cursor()
        cur.execute(f"select * from {self.table_name}")
        case_info = [list(row) for row in cur.fetchall()]
        return case_info

    def add(self, uac: str, case_info: list = None) -> None:
        super().add(uac, case_info)
        self.new_cases.append([uac, *case_info] if case_info else [uac])

    def save(self) -> None:
        insert_template = f"""
        insert into {self.table_name} ({", ".join(self.columns)})
        values ({", ".join("?" for col in self.columns)})
        """

        con = self.connect()
        cur = con.cursor()
        cur.fast_executemany = True
        cur.executemany(insert_template, self.new_cases)
        cur.commit()
        self.new_cases = list()
