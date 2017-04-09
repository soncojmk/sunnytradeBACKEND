from django.shortcuts import render
from sunnytrade.scrape import scrape_page
from sunnytrade.Robinhood import Robinhood
from .secrets import username, password

# Create your views here.

from rest_framework import views
from rest_framework.response import Response

class getScore(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        stock = request.GET.get('stock', None)
        #url = request.DATA.get('url', None)
        if stock:
            return get_sentiment(stock)
        else:
            return Response({"success": False})


class buy(views.APIView):
    permission_classes = []

    #sell_order = my_trader.place_sell_order(stock_instrument, 1)

    def post(self, request, *args, **kwargs):
        stock = request.POST.get('stock', None)
        #url = request.DATA.get('url', None)
        if stock:
            my_trader = Robinhood()
            logged_in = my_trader.login(username=username, password=password)
            stock_instrument = my_trader.instruments(stock)[0]
            quote_info = my_trader.quote_data(stock)
            buy_order = my_trader.place_buy_order(stock_instrument, 1)
            return Response({"bought ": stock, "at price": quote_info})
        else:
            return Response({"success": False})


class sell(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        stock = request.POST.get('stock', None)
        #url = request.DATA.get('url', None)
        if stock:
            my_trader = Robinhood()
            logged_in = my_trader.login(username=username, password=password)
            stock_instrument = my_trader.instruments(stock)[0]
            quote_info = my_trader.quote_data(stock)
            sell_order = my_trader.place_sell_order(stock_instrument, 1)
            return Response({"sold ": stock, "at price": quote_info})
        else:
            return Response({"success": False})


# if you want to use this scraper with the RESTful api webservice then
# change this import: from scrapers.scrape import scrape_page

BASE_URL = "http://stocktwits.com/symbol/"
BULLISH_SENTIMENT_XPATH = '//*[@id="sentiment-chart"]/div/ul/li[1]/span/text()'
BEARISH_SENTIMENT_XPATH = '//*[@id="sentiment-chart"]/div/ul/li[2]/span/text()'
FULL_NAME_XPATH = '//*[@id="top-content"]/div/div/h1/text()'
PRICE_XPATH = '//*[@id="top-content"]/div/div/div[@class="ticker-price"]/div/span[@class="price"]/text()'

BLOOMBERG_URL = "http://www.bloomberg.com/search?query=AAPL"
TITLE_XPATH = '//*[@id="content"]/div/section/section[2]/section[1]/div[2]/div[1]/article/div[1]/h1/a/text()'
ARTICLE_XPATH = '//*[@id="content"]/div/section/section[2]/section[1]/div[2]/div[1]/article/div[1]/div[2]/text()'
LINK_XPATH = '//*[@id="content"]/div/section/section[2]/section[1]/div[2]/div[1]/article/div[1]/h1/a/@href'


def get_title(ticker_symbol, page=None):
    """
    Gets the article for the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a string of the percentage of bearish sentiment as listed on a stock's StockTwits page
    """
    if page is None:
        page = scrape_page(BLOOMBERG_URL)

    sentiment = page.xpath(TITLE_XPATH)

    if not sentiment:
        return None
    else:
        return sentiment[0].replace("\n", "")

def get_link(ticker_symbol, page=None):
    """
    Gets the article for the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a string of the percentage of bearish sentiment as listed on a stock's StockTwits page
    """
    if page is None:
        page = scrape_page(BLOOMBERG_URL + ticker_symbol)

    sentiment = page.xpath(LINK_XPATH)

    if not sentiment:
        return None
    else:
        return sentiment[0].replace("\n", "")

def get_article(ticker_symbol, page=None):
    """
    Gets the article for the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a string of the percentage of bearish sentiment as listed on a stock's StockTwits page
    """
    if page is None:
        page = scrape_page(BLOOMBERG_URL + ticker_symbol)

    sentiment = page.xpath(ARTICLE_XPATH)

    if not sentiment:
        return None
    else:
        return sentiment[0].replace("\n", "")



def get_bullish_sentiment(ticker_symbol, page=None):
    """
    Gets the bullish sentiment of the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a string of the pe rcentage of bullish sentiment as listed on a stock's StockTwit's page
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    sentiment = page.xpath(BULLISH_SENTIMENT_XPATH)

    if not sentiment:
        return None
    else:
        return sentiment[0].replace("\n", "") + " Bullish"

def get_bearish_sentiment(ticker_symbol, page=None):
    """
    Gets the bearish sentiment of the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a string of the percentage of bearish sentiment as listed on a stock's StockTwits page
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    sentiment = page.xpath(BEARISH_SENTIMENT_XPATH)

    if not sentiment:
        return None
    else:
        return sentiment[0].replace("\n", "") + " Bearish"


def get_name(ticker_symbol, page=None):
    """
    Gets the bearish sentiment of the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a string of the percentage of bearish sentiment as listed on a stock's StockTwits page
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    sentiment = page.xpath(FULL_NAME_XPATH)

    if not sentiment:
        return None
    else:
        return sentiment[0].replace("\n", "")


def get_price(ticker_symbol, page=None):
    """
    Gets the bearish sentiment of the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a string of the percentage of bearish sentiment as listed on a stock's StockTwits page
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    sentiment = page.xpath(PRICE_XPATH)

    if not sentiment:
        return None
    else:
        return sentiment[0].replace("\n", "")



def get_sentiment(ticker_symbol, page=None):
    """
    Gets both the bullish and bearish sentiment of the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a tuple of strings containing both the bullish and bearish sentiment as listed on a stock's
    StockTwits page
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    #get strings
    bullish_sentiment = get_bullish_sentiment(ticker_symbol, page)
    bearish_sentiment = get_bearish_sentiment(ticker_symbol, page)
    price = get_price(ticker_symbol, page)
    name = get_name(ticker_symbol, page)

    title = get_title(ticker_symbol, page)
    article = get_article(ticker_symbol, page)
    link = get_link(ticker_symbol, page)

    my_trader = Robinhood()
    logged_in = my_trader.login(username=username, password=password)
    description = my_trader.get_fundamentals(ticker_symbol)
    news = my_trader.get_news(ticker_symbol)

    #see strings for verification
    #print(bullish_sentiment);
    #print(bearish_sentiment);

    #find digits in string
    bull=int(''.join(list(filter(str.isdigit, bullish_sentiment))))
    bear=int(''.join(list(filter(str.isdigit, bearish_sentiment))))
    #price=int(''.join(list(filter(str.isdigit, price))))
    #print(bull)
    #print(bear)



    return Response({"bullish": bull, "bearish": bear, "price":price, "name":name, "description":description, "news":news})

    '''
    if bull>bear:
        print("bull!")
        import example
    else:
        return None
    '''
    #if bullish_sentiment:
    #    return bullish_sentiment, get_bearish_sentiment(ticker_symbol, page)

    #else:
    #    return None

if __name__ == "__main__":
    # Test cases
    print(get_sentiment("AAPL"))



