import pkg_resources
import csv
import datetime as dt

class TickerData():

    def __init__(self, filename):
        self.filename = filename
        self.data = {}


    def read_data(self):
        csvin = csv.reader(open(pkg_resources.resource_filename("stockSamples26", self.filename)))
        rows = [row for row in csvin]
        del rows[0]
        for row in rows:
            row = self.clean_row(row)
            self.add_to_data(row)


    def clean_row(self, row):
        #reformat the date
        date = dt.datetime.strptime(row[0], "%Y%m%d")
        row[0] = date

        #cast numbers to floats
        for i, val in enumerate(row):
            try:
                row[i] = float(val)
            except:
                continue
        return row

    def add_to_data(self, row):
        # if ticker is not in self.data yet
        if self.data.get(row[1], None) == None:
            self.data.update({row[1]: [ [row[0]] + row[2:] ]})
        # if ticker is already in self.data yet
        else:
            self.data[row[1]].append([row[0]] + row[2:])


    def vwap(self, ticker):
        """Return the volume weighted average price (VWAP) of the stock.  In order to do this,
        first find the average price of the stock on each day.  Then, multiply that price with the
        volume on that day.  Take the sum of these values. Finally, divide that value by the sum of all the volumes.
        (note: average price for each day = (high + low + close)/3)

        Parameters:
        ticker: str - refers to a specific stock

        Return: float which is the VWAP of the stock
        """

        wtprice = 0
        vol = 0
        for item in self.data[ticker]:
            #find avg price
            avg = (item[2] + item[3] + item[4])/3
            wtprice += avg*item[5]
            vol += item[5]
        return float(wtprice/vol)


    def calc_avg_open(self, ticker):
        """Return the average opening price for the stock as a float.

        Parameters:
        ticker: str - refers to a specific stock

        Return: the average opening price of the stock
        """
        add = 0
        count = 0
        for day in self.data[ticker]:
            add += day[1]
            count += 1
        return add/count


    def find_return(self, ticker, start, end):
        """Calculates the return of the stock between two dates.
        Uses the opening price on the starting date, and the closing price on the ending date.

        Parameters:
        ticker: str - refers to a specific stock
        start: tuple - represents the start date in the format (Month,Date,Year)
        end: tuple - represents the end date in the format (Month,Date,Year)

        Return: the mathematical return (endPrice - startPrice)/startPrice. 
        """

        #find startPrice
        for item in self.data[ticker]:
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
        for item in self.data[ticker]:
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



