from setups import dcf

if __name__ == "__main__":
	# file = open("setups/stocks.txt", "r")
	# stocks = [i.strip("\n") for i in file.readlines()]
	# dcf.multi_dcfs(stocks, "stock-valuations.xlsx")
	while True:
		ticker = input("Ticker:  ")
		tgr = float(input("Terminal Growth Rate:  "))/100
		discount_rate = float(input("Min. Discount Rate:  "))/100
		print("")
		print(dcf.one_dcf(ticker, "DCF.xlsx", tgr, discount_rate))
		print("")
