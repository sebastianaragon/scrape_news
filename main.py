import requests
from lxml import html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="container"][2]//text-fill/a/@href' #el xpath original es con h2 en vez de text-fill
XPATH_LINK_TO_TITLE = '//*[@id="vue-container"]/div[3]/div[1]/div[2]/div[1]/h2/span/text()'
XPATH_LINK_TO_SUMMARY = '//div[@id="proportional-anchor-1" and @class]//div[@class="lead"]/p/text()'
XPATH_LINK_TO_BODY = '//div[@id="proportional-anchor-1" and @class]//div[@class="html-content"]/p/text()'

def parse_notice(link,today):
    try:
        response = requests.get(link)
        if response.status_code==200:
            notice=response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            print(parsed)
            
            try:
                title=parsed.xpath(XPATH_LINK_TO_TITLE)[0] #tal parece que no reconoce ese xpath
                title=title.replace('\n','')
                print(title)
                summary=parsed.xpath(XPATH_LINK_TO_SUMMARY)[0]
                print(summary)
                body=parsed.xpath(XPATH_LINK_TO_BODY)
                print(body)
            except IndexError:
                return
            
            with open(f'{today}\{title}.txt','w',encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
                    
                
        else:
            
            raise ValueError(f'Error: {response.status_code}')
        
    except ValueError as ve:
        print(ve)
    
def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
    
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_notices)
            
            today=datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
                
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            #Elevamos el error para ser capturado en el try-except, too lo que sea un error.
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()