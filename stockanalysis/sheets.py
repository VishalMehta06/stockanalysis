# Third Party Imports
import pandas
import xlwings

# Local Imports
import stockanalysis as sa

def create_workbook(path: str, sheet_name: str) -> None:
	"""
	Helper method to create a new Excel spreadsheet.

	:param path: The path including name where the file will be created at.
	:param sheet_name: The name of the first sheet that will be created.
	"""
	df = pandas.DataFrame()
	df.to_excel(excel_writer=path, sheet_name=sheet_name)

def export_dataframe(df: pandas.DataFrame, fname: str, sheet_name: str) -> None:
	"""
	Export a pandas.DataFrame to an excel spreadsheet with the proper formatting.

	:param df: The pandas.DataFrame that we want to export. This can be a financials document, 
		forecast, DCF, and so on.
	:param sheet_name: The name of the file that the pandas.DataFrame will be exported to. Must 
		end with .xlsx.
	"""
	fname = "results/" + fname
	sa.create_workbook(fname, sheet_name)
	with xlwings.App(visible=False) as app:
		wb = app.books.open(fname)
		wb.sheets(sheet_name).range("A1").value = df
		wb.sheets[0].range('A1', 'Z1000').api.HorizontalAlignment = xlwings.constants.HAlign.xlHAlignCenter
		wb.sheets[0].range('A1', 'Z1000').autofit()
		wb.save()
