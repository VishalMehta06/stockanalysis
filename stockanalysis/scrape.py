import requests
from bs4 import BeautifulSoup
import pandas
import lxml.html

def scrape_financials(ticker: str, document: int) -> pandas.DataFrame:
	"""
	Returns either the Income Statement, Balance Sheet, or Statement of Cash Flows as a pandas DataFrame.

	:param ticker: The string ticker of the company.
	:param document: An integer where 1=Income Statement, 2=Balance Sheet, 3=Statement of Cash Flows. Nothing is
		generated for other values.
	"""
	if document == 1:
		webpage = requests.get("https://stockanalysis.com/stocks/" + ticker.lower() + "/financials/")
	elif document == 2:
		webpage = requests.get("https://stockanalysis.com/stocks/" + ticker.lower() + "/financials/balance-sheet/")
	elif document == 3:
		webpage = requests.get("https://stockanalysis.com/stocks/" + ticker.lower() + "/financials/cash-flow-statement")
	else:
		return

	soup = BeautifulSoup(webpage.text, "lxml")
	find_table = soup.find("table")
	rows = find_table.find_all("tr")

	headers = [j.text.strip("\n\t ") for j in find_table.find("tr").find_all("th")]

	array = []
	for i in rows:
		table_data = i.find_all("td")
		data = [j.text.strip("\n\t ") for j in table_data]
		array.append(data)

	df = pandas.DataFrame(list(array[1::]))
	df.columns = headers
	df = df.drop(headers[-1], axis=1)
	df = df.set_index("Year Ending")

	return df

def scrape_forecast(ticker: str) -> pandas.DataFrame:
	"""
	Returns a pandas DataFrame containing analyst forecasts for Revenue and EPS as well as the # of analysts and
		the forward PE. Unfilled data will have a "-" in the field.
	
	:param ticker: The string ticker of the company.
	"""
	webpage = requests.get("https://stockanalysis.com/stocks/" + ticker.lower() + "/forecast/")
	soup = BeautifulSoup(webpage.text, "lxml")
	find_table_parent = soup.find("div", attrs={"data-test": "forecast-financial-table"})
	find_table = find_table_parent.find("table")
	rows = find_table.find_all("tr")

	headers = [j.text.strip("\n\t ") for j in find_table.find("tr").find_all("th")]

	array = []
	for i in rows:
		table_data = i.find_all("td")
		data = [j.text for j in table_data]
		array.append(data)

	df = pandas.DataFrame(list(array[1::]))
	df.columns = headers
	df = df.set_index("Year")

	return df

def scrape_statistics(ticker: str) -> dict[str:str]:
	"""
	Returns the following statistics in a dictionary:
		"beta"
		"shares-outstanding"
		"price"
	"""
	# Get the webpage as XML
	webpage = requests.get("https://stockanalysis.com/stocks/" + ticker.lower() + "/statistics/", stream=True)
	webpage.raw.decode_content = True
	tree = lxml.html.parse(webpage.raw)
	result = {}

	result["beta"] = tree.xpath(
		"/html/body/div/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/text()")[0]
	result["shares-outstanding"] = tree.xpath(
		"/html/body/div/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[2]/text()")[0]
	result["price"] = tree.xpath("/html/body/div/div[1]/div[2]/main/div[1]/div[2]/div/div[1]/text()")[0]

	return result
