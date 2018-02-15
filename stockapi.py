from bs4 import BeautifulSoup
import requests
import re


class StockApi:
    '''An API to pull data from TMXMoney'''

    def __init__(self, stock: str):

        self._url = 'https://web.tmxmoney.com/quote.php?qm_symbol='
        self._stock = stock
        # Initialize empty variables
        self._price, self._52high, self._52low, self._volume, self._change = 0, 0, 0, 0, 0
        self.update()

    def update(self):
        '''(StockApi) -> NoneType'''
        url = self._url + self._stock
        response = requests.get(url)
        if response is not None:
            html = BeautifulSoup(response.text, 'html.parser')

            # Find real-time quoted price by searching for the css
            # class .quote-price
            price = str(html.find(class_="quote-price").select("span"))

            # Get text
            price = BeautifulSoup(price, 'lxml').get_text()

            # Dirty trick to remove brackets surrounding price
            self._price = float(price[1:-1])

            # Follow similar method to find 52 week high
            weekhigh = str(html.find(class_="week-high"))

            # Separate into separate strings
            weekhigh = BeautifulSoup(weekhigh, 'lxml').stripped_strings

            # stripped_strings method is an iterative object, so need to
            # compile results into a list and return the actual number
            self._52high = return_list(weekhigh)[1]

            # Repeat for 52 week low and volume
            weeklow = str(html.find(class_="week-low"))
            weeklow = BeautifulSoup(weeklow, 'lxml').stripped_strings

            self._52low = return_list(weeklow)[1]

            volume = str(html.find(class_="quote-volume"))
            volume = BeautifulSoup(volume, 'lxml').stripped_strings

            self._volume = return_list(volume)[1]

            # Similar premise for daily change in price.
            # Default format has a ton of whitespace, so strip
            # it out.
            change = str(html.find(class_="quote-change"))
            change = BeautifulSoup(change, 'lxml').stripped_strings
            change = str(return_list(change)[1]).split()
            change = ' '.join(change)

            self._change = change

    def get_price(self):
        return self._price

    def get_data(self):
        '''(StockApi) -> str'''

        data = 'Ticker: {!s}\nPrice: {!s}\nChange: {!s}\nVolume: {!s}\n52 Week High: {!s}\n52 Week Low: {!s}\n'.format(
            self._stock, self._price, self._change, self._volume, self._52high, self._52low)

        return data

    def __str__(self):
        return self._price


def remove_tags(text):
    return re.compile(r'<[^>]+>').sub('', text)


def return_list(iterable):
    '''(iterable) -> list'''

    result = []
    for string in iterable:
        result.append(string)
    return result


if (__name__ == "__main__"):
    APH = StockApi('APH')
    print(APH.get_data())
    BNS = StockApi('BNS')
    print(BNS.get_data())
