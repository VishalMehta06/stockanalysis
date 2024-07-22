<div align="center">

# stockanalysis v1.0.0

Integrate free financial data and high level analysis to **bridge the gap** of information <br />
between corporate investors and everyday people.

[Features](#current-features) • [Usage](#usage) • [Installation](#installation) • [Documentation](#documentation)

<hr>

</div>

### Current Features

* Export **5 years** worth of data from financial statements for almost all publicly traded stocks.
* Export **analyst forecasts** of revenue and net income.
* Generate **discounted cash flow** models for companies based on analyst forecasts

### Features to Come in Later Versions 

* Maintain a **watchlist** with periodic evaluations.
* Evaluate **analyst sentiment**
* Export data from a **variety of sources** other than [stockanalysis.com](https://stockanalysis.com)

### Usage

This tool is free to use for any purposes outlined in the [MIT License](/LICENSE).

### Installation

**1.** Open terminal or command prompt

Linux:
	```
	CTRL + ALT + T
	```

Windows:
	```
	WINDOWS, "cmd", ENTER
	```

MAC:
	```
	Launchpad icon, "Terminal", <click "Terminal">
	```

**2.** Clone the GitHub repository
```
git clone https://github.com/VishalMehta06/stockanalysis.git
```

**3.** Start a venv if you would like

**4.** Run setup.py
```
cd stockanalysis
python setup.py build
```

**5.** Install stockanalysis
```
pip install stockanalysis
```

**6.** Import stockanalysis in `__main__.py`
```
import stockanalysis as sa

...

# Rest of your code
```

### Documentation

1. [Stock Object](#stock-object)
	* [Attributes](#stock-attributes)
	* [Functions](#stock-functions)


#### Stock Object
```
Stock(ticker: str,
	  terminal_growth_rate: float = 0.03,
	  min_discount_rate: float = 0.05,
	  risk_free_rate: float = 0.047,
	  market_return: float = 0.08,
	  default_beta: float = 1.3) -> None
```
```
Access historical data and analyst predictions from stockanalysis.com for any company available on the site.

:param ticker: A string containing the ticker of the company.
:param terminal_growth_rate: The terminal growth rate used if another is not generated
	when running a (discounted cash flow) DCF model.
:param min_discount_rate: The minimum discount rate allowed.
:param risk_free_rate: The risk free rate assumed. Generally return of US Treasury for desired 
	time period.
:param market_return: The expected return for the market subset that is being analyzed.
:param default_beta: The beta to use if no 5 Year beta is available on stockanalysis.com.
```
**What this does do:** 
It creates a `Stock` object that represents a `ticker` and the attributes that go along with it. 

#### Stock Attributes
* `Stock.financials: list[pandas.DataFrame]`
	* This is a list of `pandas.DataFrame`s where they are initially blank. 
		* 1st index contains the Income Statement
		* 2nd index contains the Balance Sheet
		* 3rd index contains the Statement of Cash Flows
	* These indexes are populated after running `Stock.gen_financials()` which is covered later.
	* Examples of what to expect can be found [here](https://stockanalysis.com/stocks/amzn/financials/)

* `Stock.forecast: pandas.DataFrame`
	* This is a `pandas.DataFrame` that contains analyst forecasts for revenue and earnings per share.
	* This is blank before `Stock.gen_forecast()` is called.
	* Examples of what to expect can be found [here](https://stockanalysis.com/stocks/amzn/forecast/)

* `Stock.statistics: dict[str:str]`
	* This is a dictionary that contains the following scraped data:
		* "beta": str
		* "shares-outstanding": str
		* "price": str
	* Each value is a number stored as a string.
	* This is blank before `Stock.gen_statistics` is called.
	* An example of a page from which data is scraped from can be found 
	[here](https://stockanalysis.com/stocks/amzn/statistics/)

* `Stock.dcf: pandas.DataFrame()`
	* This is a `pandas.DataFrame` that contains the generated discounted cash flow analysis.
	* Example of an output is found below:

|                      |2019  |2020  |2021  |2022  |2023  |TTM   |2024  |2025  |2026  |2027  |2028     |
|----------------------|------|------|------|------|------|------|------|------|------|------|---------|
|Revenue               |280522|386064|469822|513983|574785|590740|651010|722860|801710|884720|976250   |
|Revenue Growth        |20.45%|37.62%|21.70%|9.40% |11.83%|12.54%|13.26%|11.04%|10.91%|10.35%|10.35%   |
|Net Income            |11588 |21331 |33364 |-2722 |30425 |37684 |48198 |61211 |78387 |93482 |109826   |
|Net Margin            |4.13% |5.53% |7.1%  |-0.53%|5.29% |6.38% |7.4%  |8.47% |9.78% |10.57%|11.25%   |
|D&A                   |21789 |25180 |34433 |41921 |48663 |49224 |54564 |60942 |67987 |75467 |83763    |
|D&A % Of Revenue      |7.77% |6.52% |7.33% |8.16% |8.47% |8.33% |8.38% |8.43% |8.48% |8.53% |8.58%    |
|CAPEX                 |12689 |35044 |55396 |58321 |48133 |48998 |56795 |66332 |77379 |89817 |104245   |
|CAPEX % Of Revenue    |4.52% |9.08% |11.79%|11.35%|8.37% |8.29% |8.72% |9.18% |9.65% |10.15%|10.68%   |
|Free Cash Flow        |20688 |11467 |12401 |-19122|30955 |37910 |45967 |55821 |68995 |79132 |89344    |
|Free Cash Flow Margin |7.37% |2.97% |2.64% |-3.72%|5.39% |6.42% |7.06% |7.72% |8.61% |8.94% |9.15%    |
|Present Value of FCF  |      |      |      |      |      |      |42355 |47393 |53975 |57041 |59341    |
|Terminal Value        |      |      |      |      |      |      |      |      |      |      |1664695  |
|Present Terminal Value|      |      |      |      |      |      |      |      |      |      |1105670  |
|Enterprise Value      |      |      |      |      |      |      |      |      |      |      |1365775  |
|Cash (+)              |      |      |      |      |      |      |      |      |      |      |72852.0  |
|Debt (-)              |      |      |      |      |      |      |      |      |      |      |134686.0 |
|Market Cap            |      |      |      |      |      |      |      |      |      |      |1303941.0|
|Shares Outstanding    |      |      |      |      |      |      |      |      |      |      |10410.0  |
|Implied Share Price   |      |      |      |      |      |      |      |      |      |      |$125.26  |
|Margin of Safety      |      |      |      |      |      |      |      |      |      |      |-31.6%   |

* `Stock.price: float`
	* Contains the price of a security, default value is hard coded as 1. 
	* A price is generated when a process requires it, such as making a DCF.

* `Stock.shares_outstanding: float`
	* Contains the shares outstanding of a security, default value is hard coded as 1.
	* A value is generated when a process requires it, such as making a DCF.

* `Stock.dcf_result: float`
	* Contains the intrinsic value or implied price of a dcf, default value is hard coded as 1.
	* A value is generated after running a DCF.

* `Stock.dcf_margin: str`
	* Contains the margin of safety given by (intrinsic value - current price)/current price as a percentage.

* `Stock.ticker: str`
	* Contains the ticker passed during object initialization.

* `Stock.discount_rate: float`
	* Contains the discount rate that is treated as a minimum discount rate when calculating a DCF.

* `Stock.risk_free_rate: float`
	* Contains the risk free rate available. Often the rate of a US Treasury bond.

* `Stock.beta: float`
	* Contains the default beta if one is not found at first. 
	But after running a DCF, it will contain the real beta.

* `Stock.market_return: float`
	* Contains the average return of the market, or universe of stocks being analyzed. Default value is 0.08.

* `Stock.terminal_growth_rate: float`
	* 

#### Stock Functions
* `gen_financials(self, document: int) -> None`
	```
	"""
	Generates either the Income Statement, Balance Sheet, or Statement of Cash Flows as a pandas DataFrame.

	:param document: An integer where 1=Income Statement, 2=Balance Sheet, 3=Statement of Cash Flows. Nothing is
		generated for other values.
	"""
	```

* `gen_forecast(self) -> None`
	```
	"""
	Generates a pandas DataFrame containing analyst forecasts for Revenue and EPS as well as the # of analysts and
		the forward PE.
	"""
	```

* `gen_statistics(self) -> None`
	```
	"""
	Generates the following statistics in a dictionary self.statistics:
		"beta"
		"shares-outstanding"
		"price"
	"""
	```

* `gen_dcf(self, auto_terminal_growth_rate: bool = True, regen_dep_data = True) -> None`
	```
	"""
	Generate a DCF and its results: self.dcf (the DCF), self.dcf_margin (Margin of Safety), 
		self.dcf_result (Intrinsic Value per Share). 
	
	Also automatically generate dependent information: self.financials (Income Statement, Balance Sheet, 
		Statement of Cash Flows), self.price (Price per Share), and self.discount_rate (Discount Rate), 
		self.beta (5 Year Beta).

	:param auto_terminal_growth_rate: True = Generate terminal growth rate based on revenue estimates. 
		False = Use self.terminal_growth_rate
	
	:param regen_dep_data: True = fetch all financials, forecasts, and statistics from https://stockanalysis.com. 
		False = Use data fetched previously.
	"""
	```
