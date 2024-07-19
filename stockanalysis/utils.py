import pandas

def create_workbook(path: str, sheet_name: str):
	"""
	Helper method to create a new Excel spreadsheet.

	:param path: The path including name where the file will be created at.
	:param sheet_name: The name of the first sheet that will be created.
	"""
	df = pandas.DataFrame()
	df.to_excel(excel_writer=path, sheet_name=sheet_name)
