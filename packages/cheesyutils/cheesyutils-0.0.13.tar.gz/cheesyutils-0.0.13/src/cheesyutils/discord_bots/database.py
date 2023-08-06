import aiosqlite
from typing import Any, List, Optional, Union
from enum import Enum


"""
PRAGMA foreign_keys = 0;

CREATE TABLE cheesyutils_temp_table AS SELECT * FROM {};

DROP TABLE {};

CREATE TABLE blacklist (
    server_id INTEGER NOT NULL,
    username  TEXT    DEFAULT NULL,
    user_id   INTEGER NOT NULL,
    mod_id    INTEGER NOT NULL,
    timestamp DOUBLE  NOT NULL,
    reason    TEXT    DEFAULT NULL,
    test      CHAR
);

INSERT INTO {} (
                          server_id,
                          username,
                          user_id,
                          mod_id,
                          timestamp,
                          reason
                      )
                      SELECT server_id,
                             username,
                             user_id,
                             mod_id,
                             timestamp,
                             reason
                        FROM cheesyutils_temp_table;

DROP TABLE cheesyutils_temp_table;

PRAGMA foreign_keys = 1;
"""


class DataType(Enum):
    integer = "INTEGER"
    real = "REAL"
    blob = "BLOB"
    text = "TEXT"
    null = "NULL"


class Table:
    """Helper class to construct sql queries for tables"""

    def __init__(self, name: str):
        self._name = name
        self._columns = []
        self._has_primary_key = False

    @property
    def sql(self) -> Optional[str]:    
        return """CREATE TABLE IF NOT EXISTS {} {}""".format(self._name, "(" + (", ".join([column for column in self._columns])) + ")")
    
    def add_column(
        self,
        name: str,
        datatype: DataType,
        primary_key: Optional[bool] = False,
        unique: Optional[bool] = False,
        default: Optional[Any] = None,
        not_null: Optional[bool] = False
    ):
        sql = f"""{name} {datatype.value}"""

        if primary_key:
            if self._has_primary_key:
                raise ValueError("Primary key already exists in table")
            else:
                sql += """ PRIMARY KEY"""

        if not_null:
            sql += """ NOT NULL"""
        
        if unique:
            sql += """ UNIQUE"""
        
        if default:
            # add redundant quotes on strings
            if isinstance(default, str):
                default = f"\"{default}\""

            sql += f""" DEFAULT {default}"""


        self._columns.append(sql)
    

class Database:
    def __init__(self, fp: str):
        self.fp = fp

    async def create_table(self, table: Table):
        await self.execute(table.sql)

    async def query_first(self, sql: str, as_dict: Optional[bool] = True) -> Optional[Union[dict, list]]:
        res = await self.execute(sql, auto_commit=False, as_dict=as_dict)
        if isinstance(res, (list, tuple)):
            return res[0] if res else None
        return res
    
    async def query_all(self, sql: str, as_dict: Optional[bool] = True) -> Optional[Union[list, dict]]:
        return await self.execute(sql, auto_commit=False, as_dict=as_dict)

    async def execute(self, sql: str, auto_commit: Optional[bool] = True, as_dict: Optional[bool] = False) -> List[dict]:
        async with aiosqlite.connect(self.fp) as db:
            if as_dict:
                db.row_factory = aiosqlite.Row

            async with db.execute_fetchall(sql) as result:
                if auto_commit:
                    await db.commit()

                return result


if __name__ == "__main__":
    table = Table("test_table")
    table.add_column(name="id", datatype=DataType.integer, not_null=True, primary_key=True)
    table.add_column(name="test", datatype=DataType.real, default=0.0)
    print(table.sql)
