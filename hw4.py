#Robert Blom
#903261321

import csv
import xml.etree.ElementTree as et
import datetime as dt
def read_tree(filename):
    """This function will read in the existing xml file and return a dictionary.
    The keys to the dictionary will be the sectors found in the xml file
    The value of each key will be another dictionary!
    This dictionary's keys will be the industries that make up that particular sector.
    The value of each key will be a list of the xml elements in the original tree for the stocks
    that make up that industry.

    Parameters:
    filename: str - name of the existing xml file

    Return: dict which will be in the format above.
    """
    #Replace ampersands
    fin = open(filename)
    text = fin.read()
    text = text.replace("&", "&amp;")
    fin.close()
    fout = open("SP500_sym.xml", "w")
    fout.write(text)
    fout.close()

    #Parse it and construct the dictionary
    tree = et.parse("SP500_sym.xml")
    root = tree.getroot()
    finalDict = {}
    for child in root:
        attributes = child.attrib
        sector = attributes["sector"]
        industry = attributes["industry"]

        #sector not in finalDict
        if finalDict.get(sector, None) == None:
            beginList = []
            beginList.append(child)
            finalDict[sector] = {industry: beginList}
        #sector in finalDict
        else:
            #industry not in sector dictionary
            if finalDict[sector].get(industry, None) == None:
                newCateg = []
                newCateg.append(child)
                finalDict[sector].update({industry: newCateg})
            #industry in sector dictionary
            else:
                finalDict[sector][industry].append(child)
    return finalDict


def create_tree(xml_dict):
    """This function takes in the dictionary you created in read_tree
    Iterate through the dictionary, and create an xml tree in the format described in the assignment
    Write that tree to a file called "output.xml"

    Parameters:
    xml_dict: dict - the dictionary you created in read_tree

    Return: None
    """
    root = et.Element("SP500")

    for sector, industries in xml_dict.items():
        sectorNode = et.SubElement(root, "Sector", name = sector)
        for industry, elements in xml_dict[sector].items():
            industryNode = et.SubElement(sectorNode, "Industry", name = industry)
            for element in elements:
                elementNode = et.SubElement(industryNode, "Stock", ticker = element.attrib["ticker"])
                elementNode.text = element.attrib["name"]

    ourTree = et.ElementTree(root)
    ourTree.write("output.xml")


def read_CSV(filename):
    """This function will read in the csv file, and return a list of lists.
    Each list will be in the following format:[date, ticker, open, high, low, close, volume].
    The date should be in the form of a datetime object - (hint: look at datetime.datetime.strptime).
    The ticker should be a string. The five numbers should be floats.

    Parameters:
    filename: str - csv file to be read

    Return: a nested list in the format specified above
    """
    csvin = csv.reader(open(filename))
    rows = [row for row in csvin]
    del rows[0]
    for row in rows:
        #reformat the date
        date = dt.datetime.strptime(row[0], "%Y%m%d")
        row[0] = date

        #cast numbers to floats
        for i, val in enumerate(row):
            try:
                row[i] = float(val)
            except:
                continue
    return rows


def stock_dictionary(csv_list):
    """This function will take in the list of lists created in read_CSV and return a dictionary.
    Each key will be a stock ticker. Each value will be a list of lists, with each list in the format
    [dateObj, open, high, low, close, volume]. Each value should only contain information pertinent to
    the corresponding key.

    Parameters:
    csv_list: list - nested list that was created in read_CSV

    Return: a dictionary with the information of the nested list
    """

    finalDict = {}
    for entry in csv_list:
        if finalDict.get(entry[1], None) == None:
            dateList = []
            dateList.append(entry[0])
            startingList = []
            startingList.append(dateList + entry[2:])
            finalDict.update({entry[1]: startingList})
        #entry in finalDict
        else:
            dateList = []
            dateList.append(entry[0])
            finalDict[entry[1]].append(dateList + entry[2:])
    return finalDict


def calc_avg_open(stock_dict, ticker):
    """This function takes in the dictionary you created in stock_dictionary and a ticker.
    Return the average opening price for the stock as a float.

    Parameters:
    stock_dict: dict - created in the stock_dictionary function
    ticker: str - refers to a specific stock

    Return: float which is the average opening price of the stock
    """
    add = 0
    count = 0
    for day in stock_dict[ticker]:
        add += day[1]
        count += 1
    return add/count

def find_return(stock_dict, ticker, start, end):
    """This function takes in the stock dictionary, a ticker, and two tuples.  The tuples
    represent dates, where each item in the tuple is an int.
    It calculates the return of the stock between the two dates.  Calculate the return using
    the formula: (endPrice - startPrice)/startPrice.
    Use the opening price on the starting date, and the closing price on the ending date.
    Return this value as a float.
    In the event that there is no data for either of the two dates, print a message notifying user and
    return None.

    Parameters:
    stock_dict: dict - created in the stock_dictionary function
    ticker: str - refers to a specific stock
    start: tuple - represents the start date in the format (Month,Date,Year)
    end: tuple - represents the end date in the format (Month,Date,Year)

    Return: float of the mathematical return
    """

    #find startPrice
    for item in stock_dict[ticker]:
        day = item[0].day
        month = item[0].month
        year = item[0].year
        if day == start[1] and month == start[0] and year == start[2]:
            startPrice = item[1]
            break
    else:
        print("Start date not found")
        return None

    #find endPrice
    for item in stock_dict[ticker]:
        day = item[0].day
        month = item[0].month
        year = item[0].year
        if day == end[1] and month == end[0] and year == end[2]:
            endPrice = item[4]
            break
    else:
        print("End date not found")
        return None

    return float((endPrice - startPrice)/startPrice)


def vwap(stock_dict, ticker):
    """This function takes in the stock dictionary and a ticker.  Return the volume weighted average
    price (VWAP) of the stock.  In order to do this, first find the average price of the stock on
    each day.  Then, multiply that price with the volume on that day.  Take the sum of these values.
    Finally, divide that value by the sum of all the volumes.
    (hint: average price for each day = (high + low + close)/3)

    Parameters:
    stock_dict: dict - created in the stock_dictionary function
    ticker: str - refers to a specific stock

    Return: float which is the VWAP of the stock
    """

    wtprice = 0
    vol = 0
    for item in stock_dict[ticker]:
        #find avg price
        avg = (item[2] + item[3] + item[4])/3
        wtprice += avg*item[5]
        vol += item[5]
    return float(wtprice/vol)


def ticker_find(tree_dict, info):
    """This function takes in the dictionary created in read_tree and a tuple that contains a
    sector and an industry that belongs to that sector.  Return a list of tickers of the stocks that belong
    to that industry.

    Parameters:
    tree_dict: dict - created in the read_tree function
    info: tuple - in the format (sector, industry)

    Return: list of tickers that belong to that industry
    """

    elements = tree_dict[info[0]][info[1]]
    result = []
    for element in elements:
        result.append(element.attrib["ticker"])
    return result


def main(args):
    """This function should have perform all of the tasks outlined above.

    Parameters:
    first: str - filename of given xml file ~ (SP_500.xml for us)
    second: str - filename of given csv file ~ (SP500_ind.csv for us)
    third: str - sector name
    fourth: str - industry name
    fifth: str - name of output csv file (OPTIONAL)

    Return: none
    """
    if len(args) < 5:
        numMissing = 5-len(args)
        print("Missing",numMissing,"argument(s). Exiting program.")
        return
    try:
        sectorDict = read_tree(args[1])
        industryTicks = ticker_find(sectorDict, (args[3],args[4])) #all tickers in an industry
        create_tree(sectorDict)
        csvrows = read_CSV(args[2])
        stockdict = stock_dictionary(csvrows) #might only contain some of the tickers in the industry
    except:
        print("One of your arguments caused an error.")
        return

    for ticker in industryTicks:
        if ticker in stockdict:
            try:
                wAvgPrice = vwap(stockdict, ticker)
                avgOpen = calc_avg_open(stockdict, ticker)
            except:
                print("One of your arguments caused an error.")
                return
            if len(args) == 5:
                print([ticker, wAvgPrice, avgOpen])
            else:
                csvout = csv.writer(open(args[5], "a"))
                csvout.writerow([ticker, wAvgPrice, avgOpen])


if __name__ == "__main__":
    import sys
    main(sys.argv)
