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
        with open(self.file, "a", newline="") as f:
            new_row = [uac, *case_info] if case_info else [uac]
            filewriter = csv.writer(f)
            filewriter.writerow(new_row)


class SqlUacStore(UacStore):
    def __init__(self, connection_string: str, table_name: str, uac_length: int, case_info_columns: dict = None):
        self.connection_string = connection_string
        self.table_name = table_name
        uac_col = {"uac": f"nchar({uac_length}) not null"}
        self.columns = uac_col | case_info_columns if case_info_columns else uac_col
        self.connections = []
        self.check_table_exists()
        self.uacs = set(self.get_all_uacs())

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
        if not cur.tables(table=self.table_name, tableType='TABLE').fetchone():
            column_statements = ",\n".join(f"{key} {value}" for key, value in self.columns.items())
            create_table_query = f"""
                create table {self.table_name} (
                    {column_statements},
                    primary key (uac)
                )
            """
            cur.execute(create_table_query)
            cur.commit()

    def get_all_uacs(self):
        con = self.connect()
        cur = con.cursor()
        cur.execute(f"select uac from {self.table_name}")
        uacs = [row[0] for row in cur.fetchall()]
        return uacs

    def add(self, uac: str, case_info: list = None) -> None:
        if self.uac_exists(uac):
            raise UacExistsError
            
        insert_template = f"""
        insert into {self.table_name} ({", ".join(self.columns)}) 
        values ({", ".join("?" for col in self.columns)})
        """
        
        new_row = [uac, *case_info] if case_info else [uac]
        con = self.connect()
        cur = con.cursor()
        cur.execute(insert_template, *new_row)
        cur.commit()
        self.uacs.add(uac)
 