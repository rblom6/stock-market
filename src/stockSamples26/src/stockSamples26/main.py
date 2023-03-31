import sys
from stockSamples26.TickerTree import TickerTree
from stockSamples26.TickerData import TickerData


def main():
    """Calculates the volume weighted average price, average open price and total return of a given stock.

    Parameters:
    first: str - sector name
    second: str - industry name
    third: str - name of output csv file (OPTIONAL)

    Return: none
    """
    sector = input("Enter a sector: ")
    industry = input("Enter an industry: ")

    print("Reading ticker metadata...")
    tTree = TickerTree("data/SP_500.xml")
    tTree.read_tree()
    industryTickers = tTree.get_industry_tickers(sector, industry)

    print("Reading historical data...")
    tData = TickerData("data/SP500_ind.csv")
    tData.read_data()
    
    print("Printing ticker, weighted avg price, and avg open...")
    for ticker in industryTickers:
        if ticker in tData.data:
            try:
                wAvgPrice = tData.vwap(ticker)
                avgOpen = tData.calc_avg_open(ticker)
            except:
                print("One of your inputs caused an error.")
                return
            print([ticker, wAvgPrice, avgOpen])


if __name__ == "__main__":
    main(sys.argv)
