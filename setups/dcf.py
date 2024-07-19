# Third Party Imports
import pandas
import xlwings

# Local Imports
import stockanalysis as sa

def multi_dcfs(tickers: list[str], result_fname: str, sort: bool = True):
	"""
	Generate an Excel with a DCF for each ticker provided in stocks. If an error occurs when 
	analyzing a stock, it will not be included in the output.

	:param stocks: A List of tickers that will be analyzed.
	:param results_fname: The file name of the results excel sheet. Must end with .xlsx
	:param sort: True = Sort the results A-Z both on the Summary and individual stock sheets. 
		False = Order of tickers is maintained as provided. 
	"""
	sa.stock_list_dcf(tickers, result_fname, sort)

def one_dcf(ticker: str, results_fname: str, terminal_growth_rate: float = 0.04, 
			min_discount_rate: float = 0.05, risk_free_rate: float = 0.047, market_return: float = 0.08, 
			default_beta: float = 1.3) -> pandas.DataFrame:
	"""
	Complete a DCF for one ticker and save it to an excel file.

	:param ticker: A string containing the ticker of the company.
	:param result_fname: The Excel file name where the DCF will be saved. Must end in .xlsx 
	:param terminal_growth_rate: The terminal growth rate used in the DCF.
	:param min_discount_rate: The minimum discount rate allowed.
	:param risk_free_rate: The risk free rate assumed. Generally return of US Treasury for desired 
		time period.
	:param market_return: The expected return for the market subset that is being analyzed.
	:param default_beta: The beta to use if no 5 Year beta is available on stockanalysis.com.
	"""
	try:
		stock = sa.Stock(ticker, terminal_growth_rate, min_discount_rate, risk_free_rate, market_return, default_beta)
		stock.gen_dcf(auto_terminal_growth_rate=False)

		results_fname = "results/" + results_fname

		sa.create_workbook(results_fname, ticker.upper())
		stock.dcf

		with xlwings.App(visible=False) as app:
			wb = app.books.open(results_fname)
			wb.sheets(ticker.upper()).range("A1").value = stock.dcf
			wb.sheets(ticker.upper()).range('B1', 'Z100').api.HorizontalAlignment = xlwings.constants.HAlign.xlHAlignCenter
			wb.sheets(ticker.upper()).range('A1', 'A100').api.HorizontalAlignment = xlwings.constants.HAlign.xlHAlignLeft
			wb.sheets(ticker.upper()).range('A1', 'L1').font.bold = True
			wb.sheets(ticker.upper()).range('A1', 'A100').font.bold = True
			wb.sheets(ticker.upper()).range('L20', 'L21').font.bold = True
			wb.sheets(ticker.upper()).range('A1', 'Z100').autofit()
			wb.save()
		return stock.dcf
	except:
		print(f"~~ An error has occurred, the DCF for {ticker.upper()} is unavailable ~~")
