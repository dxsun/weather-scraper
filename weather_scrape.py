
# coding: utf-8

# In[44]:

from bs4 import BeautifulSoup as BS 
import requests as req 

print("Which city would you like to get the weather for today?")
city = input("0 - San Francisco, 1 - Cambridge\n")

cities = {0: 'San Francisco', 1: 'Cambridge'}

weather_url = {0: 'https://weather.com/weather/tenday/l/USCA0987:1:US',
			   1: 'https://weather.com/weather/tenday/l/USMA0066:1:US'}
try:
	page = req.get(weather_url[int(city)])
except KeyError:
	print('ERROR - City URL either doesn\'t exist or wrong input')
	raise

soup = BS(page.content, 'html.parser')
dates = soup.find_all('span', class_='day-detail clearfix')
days = soup.find_all('span', class_='date-time')

bodies = soup.find_all('tr', class_='clickable closed')


from tabulate import tabulate
import unicodedata

headers = ['Day', 'Date', 'Description', 'High/Low', 'Precipitation', 'Wind', 'Humidity']
data = []

for body in bodies:
    date_time = body.find('span', class_='date-time').get_text()
    day_detail = body.find('span', class_='day-detail clearfix').get_text()
    description = body.find('td', class_='description').find('span').get_text()
    temp_high = body.find('td', class_='temp').find_all('span')[0].get_text()
    temp_low = body.find('td', class_='temp').find_all('span')[2].get_text()
    precip = unicodedata.normalize("NFKD", body.find('td', class_='precip').get_text())
    wind = body.find('td', class_='wind').get_text()
    humid = body.find('td', class_='humidity').get_text()
    
    data.append([date_time, day_detail, description, temp_high + '/' + temp_low, str(precip), wind, humid])

print("{}'s weather for upcoming days\n\n".format(cities[int(city)]))
print(tabulate(data, headers))




