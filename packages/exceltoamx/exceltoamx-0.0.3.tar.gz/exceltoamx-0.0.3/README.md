# exceltoamx
import excel spreadsheet to list of amx dicts.

This is NOT a generic Excel importer. It's specific to campus AMX systems.

Each amx system is represented by a dictionary populated by the excel columns.
These dictionaries are then put into a single list and returned.

Required columns:
	building_name,
	room_number,
	master_ip

Columns handled here but not required:
	system_number,
	space_use_code,
	tp_generation

Any additional columns are allowed. They will be converted to dict k,v pairs

Requires tablib. Dictionary keys are populated from the top row of data in
the .xlsx file.
Each additional row is turned into a dictionary with the values from that row.
Then all of the rows/dictionaries are put into a list and returned.
We could also return the xlsx dataset, but there's no current use for it so
I left that commented out.
:param path: path to .xlsx file
:return: list of dictionaries
