import requests
import smtplib
from datetime import date, timedelta

#Taking stock data from https://www.alphavantage.co
STOCK_NASDAQ = "AMZN"
COMPANY_NAME = "Amazon.com, Inc."
alphavantage_api_key = 'alphavantagekey'

stock_parameters = {
  'symbol' : STOCK_NASDAQ,
  'function' : 'TIME_SERIES_DAILY',
  'apikey' : alphavantage_api_key
}
response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
response.raise_for_status()
data = response.json()
#print(data)


#Collecting closure prices from data
closing_prices = []
for day, day_data in data["Time Series (Daily)"].items():
    close = day_data["4. close"]
    closing_prices.append(close)

#print(closing_prices)


#Check if there is a significant(more than 5%) change in price 
get_news = False
if abs(float(closing_prices[0])/float(closing_prices[6]) - 1) > 0.05:
    get_news = True

stock_change = float(closing_prices[0])/float(closing_prices[6])
if stock_change > 1:
    stock_change = "growth: " + str((stock_change - 1)*100) + "%"
else:
    stock_change = "drop: " + str((1 - stock_change)*100) + "%"


#Check news that could have caused that change in price using https://newsapi.org
newsapi_key = "newsapikey"
today = date.today()
yesterday = today - timedelta(days=1)
news_parameters = {
  'q' : "Amazon",
  'from' : yesterday,
  'apiKey' : newsapi_key,
  'sortBy' : 'popularity',
  'language' : 'en',
  'pageSize' : '5',
  'page' : 1
}

if get_news:
    response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    response.raise_for_status()
    data = response.json()
    news_text = []
    for article in data['articles'][:6]:
        title = article['title']
        url = article['url']
        t_u = title + " " + url
        news_text.append(t_u)



#Sending email with this information
my_email = "your_email@gmail.com"
my_password = "app_password"
'''
if get_news:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs=my_email, 
            msg=f"Subject:Stock changes for Amamzon\n\nAmazon stock have {stock_change}. Top 5 news:\n {news_text[0]}\n {news_text[1]}\n {news_text[2]}\n {news_text[3]}\n {news_text[4]}")

'''       

msg=f"Subject:Stock changes for Amamzon\n\nAmazon stock have {stock_change}. Top 5 news:\n {news_text[0]}\n {news_text[1]}\n {news_text[2]}\n {news_text[3]}\n {news_text[4]}"
print(msg)       


