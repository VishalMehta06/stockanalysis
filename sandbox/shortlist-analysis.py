import radius.src.radius as radius

file = open("stocks.txt", "r")
stocks = [i.strip("\n") for i in file.readlines()]
file.close()
radius.stock_list_dcf(stocks, "buffet-strats.xlsx")
