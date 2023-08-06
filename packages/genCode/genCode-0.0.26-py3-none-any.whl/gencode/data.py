from db_hammer.util.date import date_to_str

from gencode.db import get_all_tables, get_columns_by_table
from gencode.models import Table, Column
from gencode.utils import *

is_debug = True


def get_data(table_name=None):
    from gencode.config import myself
    objs = get_all_tables()
    ts = []
    c_table = Table()
    for obj in objs:
        table = Table()
        table.comment = obj["comment"]
        table.XX_TABLE_NAME = str(obj["table_name"]).upper()
        table.xx_table_name = str(obj["table_name"]).lower()
        table.XxTableName = get_XxTableName(obj["table_name"])
        table.xxTableName = get_xxTableName(obj["table_name"])
        table.xxtablename = table.xxTableName.lower()
        table.XXTABLENAME = table.xxTableName.upper()
        table.XX = get_table_package(obj["table_name"]).upper()
        table.xx = get_table_package(obj["table_name"]).lower()

        table.table_name = get_table_name(obj["table_name"])
        table.TABLE_NAME = str(table.table_name).upper()
        table.tableName = get_TableName(obj["table_name"]).lower()
        table.tableName = get_tableName(obj["table_name"])
        table.TableName = get_TableName(obj["table_name"])
        table.columns = []

        if table_name is not None and table_name.lower() == table.xx_table_name:
            cols = get_columns_by_table(table_name)
            del_same_colname={}
            for c in cols:
                column = Column()
                column.comment = c["comment"]
                column.db_dataType = c["data_type"]
                column.dataType = get_dataType(c["data_type"], c["data_length"])
                column.data_length = c["data_length"]
                column.column_name = str(c["column_name"]).lower()
                column.COLUMN_NAME = str(c["column_name"]).upper()
                column.ColumnName = get_ColumnName(c["column_name"])
                column.columnName = get_columnName(c["column_name"])
                column.columnname = get_columnName(c["column_name"]).lower()
                column.COLUMNNAME = get_columnName(c["column_name"]).upper()
                column.is_pk = bool(c["is_pk"])
                table.columns.append(column)
            c_table = table
        ts.append(table)

    print_tables(ts)

    d = {
        "tables": ts,
        "date": date_to_str(format_str="%Y-%m-%d"),
        "datetime": date_to_str(),
        "author": myself.get("author", ""),
        "mail": myself.get("mail", ""),
        "sign": myself.get("sign", ""),

    }
    d.update(c_table.__dict__)

    return d


def print_tables(ts):
    global IS_DEBUG
    from rich.console import Console
    from rich.table import Table as pTable
    console = Console()
    table = pTable(show_header=True, header_style="bold magenta")
    table.add_column("ColumnName")
    table.add_column("DB_DataType")
    table.add_column("DataType")
    table.add_column("DataLength")
    table.add_column("PK")
    table.add_column("Comment")
    for t in ts:
        table.rows.clear()

        c: Column = None
        for c in t.columns:
            table.add_row(c.column_name, c.db_dataType, c.dataType, str(c.data_length), "Y" if c.is_pk else '',
                          c.comment)
        if len(table.rows) > 0 and is_debug:
            console.print(t.XX_TABLE_NAME + "  " + t.comment, style="bold blue")
            console.print(table)
