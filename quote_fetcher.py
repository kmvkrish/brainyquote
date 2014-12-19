import requests
from lxml import html
import time
import string

def fetch_links(topic):
    url = "http://brainyquote.com"+topic
    page = requests.get(url)
    print page.url,"\n"
    tree = html.fromstring(page.text)
    end = tree.xpath('/html/body/div[4]/div/div/div[1]/div[2]/div/ul[2]/li[1]/div/ul/li[last()-1]/a/text()')
    #print end[0],"\n"
    for link in range(1,int(end[0])+1):
        if link == 1:
            fetch_quotes(url)
        else:
            blink = url.split('.html')
            fetch_quotes(string.replace(url,url,"%s%s.html"%(blink[0],link)))

def fetch_quotes(url):
    page = requests.get(url)
    print "\t\tFetching quotes from ",page.url,"\n"
    tree = html.fromstring(page.text)
    f = open("quotes.txt","a+")
    for quotes in tree.xpath('//div[@id="quotesList"]//span[@class="bqQuoteLink"]/a/text()'):
        #print quotes,"\n"
        f.write(quotes.encode('utf-8')+"\n")
    f.close()

def get_topics():
    page = requests.get('http://www.brainyquote.com/quotes/topics.html')
    tree = html.fromstring(page.text)
    topics = tree.xpath('//div[@class="bqLn"]/div[@class="bqLn"]/a/@href')
    for topic in topics:
        #print topic,"\n"
        fetch_links(topic)
        time.sleep(5)

if __name__ == '__main__':
    get_topics()
