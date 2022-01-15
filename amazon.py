from requests_html import HTMLSession
import pandas as pd
from time import sleep
from tqdm import tqdm

s = HTMLSession()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Connection':'keep-alive'
}


def pages(x):
    url = f'https://www.amazon.in/s?k={query}&page={x}'
    r = s.get(url, headers=headers)
    r.html.render(sleep=1, timeout=100)
    content = r.html.find('div[data-asin]')
    links = []
    for item in content:
        if item.attrs['data-asin'] != '':
            urls = 'https://www.amazon.in/dp/' + item.attrs['data-asin']
            links.append(urls)
    return links


def get_product_data(link):
    r = s.get(link)
    r.html.render(sleep=1, timeout=100)
    container = r.html.find('div#dp-container')
    for item in container:
        try:
            ti = item.find('span#productTitle', first=True).text
        except:
            ti = ''
        try:
            rat = item.find('span.a-icon-alt', first=True).text.replace('out of 5 stars', '')
        except:
            rat = ''
        try:
            revrat = item.find('span#acrCustomerReviewText', first=True).text.replace('ratings', '')
        except:
            revrat = ''
        try:
            aq = item.find('a#askATFLink span', first=True).text.replace('answered questions', '')
        except:
            aq = ''
        try:
            mrp = item.find('span.a-price.a-text-price.a-size-base span', first=True).text.replace('₹', '')
        except:
            mrp = ''
        try:
            dd = item.find('span.a-price.a-text-price.a-size-medium.apexPriceToPay span', first=True).text.replace('₹', '')
        except:
            dd = ''
        try:
            url = link
        except:
            url = ''
            
        dic = {
            'Product':ti,
            'Star_Rating':rat,
            'Review_Rating':revrat,
            'Answered_Questions':aq,
            'MRP':mrp,
            'Deal_Price':dd,
            'Url':url
        }

    return dic


query=input('Enter product name: ')
mainlist = []
for x in tqdm(range(1, 11)):
    links = pages(x)
    for link in tqdm(links):
        mainlist.append(get_product_data(link))


df = pd.DataFrame(mainlist)
df.to_csv(f'{query}'+'.csv', index=False)


input()
