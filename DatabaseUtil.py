#!/bin/python3
import pymysql
from collections.abc import Iterable

def cleanDatabaseTable(cursor, tableName, ids = None):
	cursor.execute(f"""
		SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
		WHERE TABLE_NAME = "{tableName}" AND DATA_TYPE = "point"
	""")
	mysqlType_point = list(map(lambda x: x["COLUMN_NAME"], cursor.fetchall()))
	cursor.execute(f"CREATE TEMPORARY TABLE temp_{tableName} AS SELECT * FROM {tableName}")
	for item in mysqlType_point:
		cursor.execute(f"""
			ALTER TABLE temp_{tableName} ADD COLUMN temp_{item} VarChar(16) AFTER {item}
		""")
		cursor.execute(f"""
			UPDATE temp_{tableName} 
			SET temp_{item} = CONCAT(
				"(", st_x({item}), ", ", st_y({item}), ")"
			)
		""")
		cursor.execute(f"ALTER TABLE temp_{tableName} DROP COLUMN {item}")
		cursor.execute(f"ALTER TABLE temp_{tableName} RENAME COLUMN temp_{item} TO {item}")
	if ids == None:
		cursor.execute(
			f"SELECT * FROM temp_{tableName}", 
			[]
		)
	elif type(ids) == int:
		cursor.execute(
			f"SELECT * FROM temp_{tableName} WHERE id=%s",
			[ids]
		)
	elif isinstance(ids, Iterable):
		cursor.execute(
			f"SELECT * FROM temp_{tableName} WHERE id=%s",
			[ids]
		)
	else:
		raise KeyError(f"Arg `ids` type excepted in [NoneType, int, ∈collections.abs.Iterable], got {type(ids)}")
	return cursor.fetchall()

