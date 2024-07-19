from setups.dcf import multi_dcfs
from setups.dcf import one_dcf

if __name__ == "__main__":
	# file = open("setups/stocks.txt", "r")
	# stocks = [i.strip("\n") for i in file.readlines()]
	# multi_dcfs(stocks, "stock-valuations.xlsx")
	print(one_dcf("payc", "PAYC DCF.xlsx", 0.03, 0.08))
