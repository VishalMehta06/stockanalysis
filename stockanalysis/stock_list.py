# Third Party Imports
import pandas
import xlwings

# Local Imports
import stockanalysis as sa

def stock_list_dcf(tickers: list[str], results_fname: str, sort: bool = True) -> None:
	"""
	Complete a Discounted Cash Flow for each ticker in tickers. Each stock will have their own DCF appear in a 
		separate sheet in the same file. There will also be a summary page containing the highlights of the 
		results of each stock.

	:param tickers: This list of strings contains all tickers that will be evaluated.
	:param results_fname: The file name of the results excel sheet. Must end with .xlsx
	:param sort: True = Sort the results A-Z both on the Summary and individual stock sheets. 
		False = Order of tickers is maintained as provided.
	"""
	df = pandas.DataFrame(columns=["#", "Ticker", "Price", "Discount Rate", "Terminal Growth Rate", "Margin"])
	results_fname = "results/" + results_fname

	with xlwings.App(visible=False) as app:
		try:
			wb = app.books.open(results_fname)
			current_sheets = [sheet.name for sheet in wb.sheets]
		except:
			sa.create_workbook(results_fname, "Summary")
			wb = app.books.open(results_fname)
			current_sheets = [sheet.name for sheet in wb.sheets]

	if sort:
		tickers.sort()

	count = 1
	for i in range(len(tickers)):
		ticker = tickers[i]
		stock = sa.Stock(ticker)
		try:
			stock.gen_dcf()
			df.loc[i] = [count, ticker.upper(), "$"+str(stock.price), str(stock.discount_rate*100)+"%", str(stock.terminal_growth_rate*100)+"%", stock.dcf_margin]

			with xlwings.App(visible=False) as app:
				wb = app.books.open(results_fname)
				if ticker.upper() in current_sheets:
					wb.sheets(ticker.upper()).range("A1").value = stock.dcf
				else:
					new_sheet = wb.sheets.add(after=wb.sheets.count)
					new_sheet.range("A1").value = stock.dcf
					new_sheet.name = ticker.upper()
				wb.sheets(ticker.upper()).range('B1', 'Z100').api.HorizontalAlignment = xlwings.constants.HAlign.xlHAlignCenter
				wb.sheets(ticker.upper()).range('A1', 'A100').api.HorizontalAlignment = xlwings.constants.HAlign.xlHAlignLeft
				wb.sheets(ticker.upper()).range('A1', 'L1').font.bold = True
				wb.sheets(ticker.upper()).range('A1', 'A100').font.bold = True
				wb.sheets(ticker.upper()).range('L20', 'L21').font.bold = True
				wb.sheets(ticker.upper()).range('A1', 'Z100').autofit()
				wb.save()
			count += 1
			print(f"[*] {ticker.upper()} is Complete")
		except:
			print(f"~~ An Error Has Occurred, {ticker.upper()} Unavailable ~~")

	df = df.set_index("#")
	with xlwings.App(visible=False) as app:
		wb = app.books.open(results_fname)
		if "Summary" in current_sheets:
			wb.sheets("Summary").range("A1").value = df
		else:
			new_sheet = wb.sheets.add(before=wb.sheets[0])
			new_sheet.range("A1").value = df
			new_sheet.name = "Summary"
		wb.sheets[0].range('A1', 'Z1000').api.HorizontalAlignment = xlwings.constants.HAlign.xlHAlignCenter
		wb.sheets[0].range('A1', 'F1').font.bold = True
		wb.sheets[0].range('A1', 'Z1000').autofit()
		wb.save()

	print(df)
