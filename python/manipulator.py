
from bs4 import BeautifulSoup

ARTICLE_BOX = 'css-1dbjc4n r-j7yic r-qklmqi r-1adg3ll r-1ny4l3l'
TWEET_USER_BOX = 'css-901oao css-bfa6kz r-18jsvk2 r-1qd0xha r-a023e6 r-b88u0q r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0'
TWEET_TEXT_BOX = 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'
TWEET_DATE_BOX = 'time'
TWEET_REPLY_BOX = 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'
TWEET_LIKE_BOX = 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'
TWEET_REPOST_BOX = 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'

def extract_information_div(div_element):

    try:

        return [
            (div_element.find('div', class_=TWEET_TEXT_BOX)).get_text(),
            (div_element.find('div', class_=TWEET_USER_BOX)).get_text(),
            (div_element.find(TWEET_DATE_BOX))['datetime'],
            ((div_element.find_all('div', {'role' : 'group'}))[0].find_all('span', class_=TWEET_REPLY_BOX)[0]).get_text(), 
            ((div_element.find_all('div', {'role' : 'group'}))[0].find_all('span', class_=TWEET_REPLY_BOX)[1]).get_text(),
            ((div_element.find_all('div', {'role' : 'group'}))[0].find_all('span', class_=TWEET_REPLY_BOX)[2]).get_text()         
        ]

    except IndexError:

        return [
            (div_element.find('div', class_=TWEET_TEXT_BOX)).get_text(),
            (div_element.find('div', class_=TWEET_USER_BOX)).get_text(),
            (div_element.find(TWEET_DATE_BOX))['datetime'],
            '0',
            '0',
            '0' 
        ]

