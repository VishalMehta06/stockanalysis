# Third-party imports
import pandas

# Local Imports
import stockanalysis as sa


class Stock:
	def __init__(self, ticker: str, terminal_growth_rate: float = 0.03, min_discount_rate: float = 0.05, 
			     risk_free_rate: float = 0.047, market_return: float = 0.08, default_beta: float = 1.3) -> None:
		"""
		Access historical data and analyst predictions from stockanalysis.com for any company available on the site.

		:param ticker: A string containing the ticker of the company.
		:param terminal_growth_rate: The terminal growth rate used if another is not generated
		 	when running a DCF.
		:param min_discount_rate: The minimum discount rate allowed.
		:param risk_free_rate: The risk free rate assumed. Generally return of US Treasury for desired 
			time period.
		:param market_return: The expected return for the market subset that is being analyzed.
		:param default_beta: The beta to use if no 5 Year beta is available on stockanalysis.com.
		"""
		self.financials = [pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame()]
		self.forecast = pandas.DataFrame()
		self.statistics = {}
		self.dcf = pandas.DataFrame()
		self.price = 1
		self.shares_outstanding = 1
		self.dcf_result = 1
		self.dcf_margin = "1%"

		self.ticker = ticker.lower()
		self.discount_rate = min_discount_rate
		self.risk_free_rate = risk_free_rate
		self.beta = default_beta
		self.market_return = market_return
		self.terminal_growth_rate = terminal_growth_rate

	def gen_financials(self, document: int) -> None:
		"""
		Generates either the Income Statement, Balance Sheet, or Statement of Cash Flows as a pandas DataFrame.

		:param document: An integer where 1=Income Statement, 2=Balance Sheet, 3=Statement of Cash Flows. Nothing is
			generated for other values.

			* Generally will be provided by stockanalysis.INCOME_STATEMENT, stockanalysis.BALANCE_SHEET, 
			stockanalysis.CASH_FLOW_STATEMENT, with the correct number being supplied for each document.
		"""
		self.financials[document-1] = sa.scrape_financials(self.ticker, document)

	def gen_forecast(self) -> None:
		"""
		Generates a pandas DataFrame containing analyst forecasts for Revenue and EPS as well as the # of analysts and
			the forward PE.
		"""
		self.forecast = sa.scrape_forecast(self.ticker)
	
	def gen_statistics(self) -> None:
		"""
		Generates the following statistics in a dictionary self.statistics:
			"beta"
			"shares-outstanding"
			"price"
		"""
		self.statistics = sa.scrape_statistics(self.ticker)

	def gen_dcf(self, auto_terminal_growth_rate: bool = True, regen_data = True) -> None:
		"""
		Generate a DCF and its results: self.dcf (the DCF), self.dcf_margin (Margin of Safety), 
			self.dcf_result (Intrinsic Value per Share). 
		
		Also automatically generate dependent information: self.financials (Income Statement, Balance Sheet, 
			Statement of Cash Flows), self.price (Price per Share), and self.discount_rate (Discount Rate), 
			self.beta (5 Year Beta).

		:param auto_terminal_growth_rate: True = Generate terminal growth rate based on revenue estimates. 
			False = Use self.terminal_growth_rate
		
		:param regen_data: True = fetch all financials, forecasts, and statistics from https://stockanalysis.com. 
			False = Use data fetched previously.
		"""
		# Get Historic and Current Data
		if regen_data:
			self.gen_financials(sa.INCOME_STATEMENT)
			self.gen_financials(sa.BALANCE_SHEET)
			self.gen_financials(sa.CASH_FLOW_STATEMENT)
			self.gen_forecast()
			self.gen_statistics()

		# Establish Assumptions
		try:
			self.beta = float(self.statistics["beta"])
		except:
			pass

		self.price = self.normalize_num(self.statistics["price"])
		self.shares_outstanding = self.normalize_num(self.statistics["shares-outstanding"])

		self.discount_rate = max(self.risk_free_rate + self.beta*(self.market_return - self.risk_free_rate), 
						   		 self.discount_rate)

		# Revenue + Revenue Growth %
		revenue = [i for i in self.forecast.iloc[0].to_list()[5::]]
		for i in range(len(revenue)):
			if revenue[i] == "-":
				revenue[i] = revenue[i-1]
			else:
				revenue[i] = round(self.normalize_num(revenue[i]))
		revenue_growth = self.forecast.iloc[1].to_list()[5::]

		# Net Income + Margin
		net_income = [round(self.shares_outstanding * self.normalize_num(i)) for i in self.forecast.iloc[2].tolist()[5::]]
		net_margin = [str(round((net_income[i]/revenue[i])*100, 2)) + "%" for i in range(len(net_income))]

		# Historic D&A and CAPEX Data and Rates of Change
		past_da = [round(self.normalize_num(i)) for i in self.financials[2].loc["Depreciation & Amortization"]][::-1]
		past_capex = [round(-self.normalize_num(i)) for i in self.financials[2].loc["Capital Expenditures"]][::-1]
		try:
			past_revenue = [round(self.normalize_num(i)) for i in self.financials[0].loc["Revenue"]][::-1]
		except:
			past_revenue = [round(self.normalize_num(i)) for i in self.financials[0].loc["Total Revenue"]][::-1]
		past_capex_margin = [round(past_capex[i]/past_revenue[i], 6) for i in range(len(past_capex))]
		past_da_margin = [round(past_da[i]/past_revenue[i], 6) for i in range(len(past_da))]
		annualized_da_change = (past_da_margin[-1]/past_da_margin[0])**(1/6) - 1
		annualized_capex_change = (past_capex_margin[-1]/past_capex_margin[0])**(1/6) - 1

		# D&A and CAPEX
		da_margin = [round(past_da_margin[-1]*((1+annualized_da_change)**((i+1)/2)), 6) for i in range(len(net_income))]
		da = [round(revenue[i]*da_margin[i]) for i in range(len(da_margin))]
		capex_margin = [round(past_capex_margin[-1]*((1+annualized_capex_change)**((i+1)/2)), 6) 
				  		for i in range(len(net_income))]
		capex = [round(revenue[i]*capex_margin[i]) for i in range(len(capex_margin))]

		# Free Cash Flow
		past_net_income = [round(self.normalize_num(i)) for i in self.financials[0].loc["Net Income"]][::-1]

		past_free_cash_flow = [past_net_income[i] + past_da[i] - past_capex[i] for i in range(len(past_net_income))]
		past_free_cash_flow_margin = [str(round((past_free_cash_flow[i]/past_revenue[i]) * 100, 2)) + "%" 
									  for i in range(len(past_free_cash_flow))]
		
		free_cash_flow = [net_income[i] + da[i] - capex[i] for i in range(len(net_income))]
		free_cash_flow_margin = [str(round(free_cash_flow[i]/revenue[i] * 100, 2)) + "%" 
						   		 for i in range(len(free_cash_flow))]

		# Formating
		past_da_margin = [str(round(i*100, 2)) + "%" for i in past_da_margin]
		da_margin = [str(round(i*100, 2)) + "%" for i in da_margin]
		past_capex_margin = [str(round(i*100, 2)) + "%" for i in past_capex_margin]
		capex_margin = [str(round(i*100, 2)) + "%" for i in capex_margin]
		past_revenue_growth = [i for i in self.financials[0].loc["Revenue Growth (YoY)"]][::-1]
		past_net_margin = [str(round(past_net_income[i]/past_revenue[i] * 100, 2)) + "%" 
					 	   for i in range(len(past_revenue))]

		# Terminal Value
		if auto_terminal_growth_rate:
			for i in range(len(revenue_growth)-1, 0, -1):
				if revenue_growth[i] != "-":
					self.terminal_growth_rate = min(
						round(float(revenue_growth[i].strip("%"))/250, 6), 
						self.terminal_growth_rate)
					break
		terminal_value = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + \
			[round(free_cash_flow[-1]*(1+self.terminal_growth_rate)/(self.discount_rate-self.terminal_growth_rate))]

		# Discounting and Final Value
		present_free_cash_flow = ["" for _ in range(len(past_free_cash_flow))] + \
			[round(free_cash_flow[i]/((1+self.discount_rate)**(i+1))) for i in range(len(free_cash_flow))]
		present_terminal_value = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + \
			[round(terminal_value[-1]/((1+self.discount_rate)**len(free_cash_flow)))]

		enterprise_value = sum([i if i != "" else 0 for i in present_free_cash_flow]) + \
						   sum([i if i != "" else 0 for i in present_terminal_value])
		try:
			debt = self.normalize_num(list(self.financials[1].loc["Long-Term Debt"])[0])
		except:
			debt = self.normalize_num(list(self.financials[1].loc["Total Debt"])[0])
		cash = self.normalize_num(list(self.financials[1].loc["Cash & Equivalents"])[0])
		marketcap = enterprise_value + cash - debt

		self.dcf_result = round(marketcap / self.shares_outstanding, 2)
		self.dcf_margin = str(round(((self.dcf_result/self.price) -1)* 100, 2)) + "%"

		# Set Up DCF
		df = pandas.DataFrame(columns=([i[-4::] for i in list(self.financials[0].columns[::-1])] + \
								 list(self.forecast.columns[5::])))
		df.loc["Revenue"] = past_revenue + revenue
		df.loc["Revenue Growth"] = past_revenue_growth + revenue_growth
		df.loc["Net Income"] = past_net_income + net_income
		df.loc["Net Margin"] = past_net_margin + net_margin
		df.loc["D&A"] = past_da + da
		df.loc["D&A % Of Revenue"] = past_da_margin + da_margin
		df.loc["CAPEX"] = past_capex + capex
		df.loc["CAPEX % Of Revenue"] = past_capex_margin + capex_margin
		df.loc["Free Cash Flow"] = past_free_cash_flow + free_cash_flow
		df.loc["Free Cash Flow Margin"] = past_free_cash_flow_margin + free_cash_flow_margin
		df.loc["Present Value of FCF"] = present_free_cash_flow
		df.loc["Terminal Value"] = terminal_value
		df.loc["Present Terminal Value"] = present_terminal_value
		df.loc["Enterprise Value"] = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + \
									 [enterprise_value]
		df.loc["Cash (+)"] = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + [cash]
		df.loc["Debt (-)"] = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + [debt]
		df.loc["Market Cap"] = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + [marketcap]
		df.loc["Shares Outstanding"] = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + \
									   [self.shares_outstanding]
		df.loc["Implied Share Price"] = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + \
										["$"+str(self.dcf_result)]
		df.loc["Margin of Safety"] = ["" for _ in range(len(past_free_cash_flow) + len(free_cash_flow)-1)] + \
									 [self.dcf_margin]

		self.dcf = df

	def normalize_num(self, value: str) -> float:
		"""
		Provide a string number with a unit at the end, and get the float version of the number in millions without extra units. 
		EX) 100B, 10M, 7.89B

		NOTE: Financials Documents are already in millions of dollars for all dollar values.

		:param value: A string number with a unit at the end like B (billions) or M (millions).
		"""
		if value == "-":
			return 0
		if value[-1] == "B":
			return float(value[0:(len(value) - 1)].replace(",", "")) * 1000
		if value[-1] == "M":
			return float(value[0:(len(value) - 1)].replace(",", ""))
		return float(value.replace(",", ""))
