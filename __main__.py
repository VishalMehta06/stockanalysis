import stockanalysis as sa

if __name__ == "__main__":
	while True:
		ticker = input("Ticker:  ")
		tgr = float(input("Terminal Growth Rate:  "))/100
		discount_rate = float(input("Min. Discount Rate:  "))/100
		print("")
		try:
			print(sa.single_dcf(ticker, terminal_growth_rate=tgr, min_discount_rate=discount_rate))
		except:
			print("~~ ERROR ~~")
		print("")
