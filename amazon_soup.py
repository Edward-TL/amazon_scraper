from bs4 import BeautifulSoup
import lxml.html as html
from lxml import etree

import re , datetime, os

import requests
from urllib.request import urlopen


def extract_soup(url, preview="True"):
    response = requests.get(url)
    print(f'Request status: {response.status_code}\n')

    # best_sells_url = 'https://www.amazon.com.mx/gp/bestsellers/?ref_=nav_cs_bestsellers'
    # best_sells_response = requests.get(best_sells_url)
    # print(f'Request status: {best_sells_response.status_code}')

    soup = BeautifulSoup(response.text, 'lxml')
    if preview==True:
        print(s.prettify())

    return soup

def amazon_raw_crawl(soup):

    #Extract Information from Soup
    ranks_soup = soup.find_all('span', attrs={'class':'zg-badge-text'})
    products_and_image = soup.find_all('div', attrs={'class' : 'a-section a-spacing-small'})
    star_ratings_soup = soup.find_all('span', attrs={'class' : 'a-icon-alt'})
    reviews_soup = soup.find_all('a', attrs={'class' : 'a-size-small a-link-normal'})
    authors_soup = soup.find_all('span', attrs={'class' : 'a-size-small a-color-base'})
    editions_soup = soup.find_all('span', attrs={'class' : 'a-size-small a-color-secondary'})

    #Extract information from Raw Arrays
    ranks = [rank.get_text() for rank in ranks_soup]
    product_names = [product_name.img.get('alt') for product_name in products_and_image]
    image_urls = [image_url.img.get('src') for image_url in products_and_image]
    star_ratings = [star_rating.get_text() for star_rating in star_ratings_soup]
    reviews = [review.get_text() for review in reviews_soup]
    authors_company = [author.get_text() for author in authors_soup]
    editions_console = [edition.get_text() for edition in editions_soup]

    soup_dict = {"Rank" : ranks,
    "Product Names": product_names, 
    "Image urls": image_urls,
    "Stars": star_ratings,
    "Reviews": reviews,
    "Authors/Company": authors_company,
    "Edition/Console": editions_console
    }

    # print(f'ranks guardados: {len(ranks)}\n')
    # print(f'product_names guardados: {len(product_names)}')
    # print(f'image_urls guardados: {len(image_urls)}')
    # print(f'star_ratings guardados: {len(star_ratings)}')
    # print(f'reviews guardados: {len(reviews)}')
    # print(f'authors_company guardados: {len(authors_company)}')
    # print(f'editions_console guardados: {len(editions_console)}')

    return soup_dict

if __name__=='__main__':

    URL_dict = {'AMZ_Mex' : 'https://www.amazon.com.mx/',
            'top_kindle' : 'https://www.amazon.com.mx/gp/bestsellers/digital-text/ref=zg_bs_digital-text_home_all?pf_rd_p=01d2df49-74bd-42d3-a898-95a4f3beb031&pf_rd_s=center-4&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=6APAMAKKFSPVHG8MWSXT&pf_rd_r=6APAMAKKFSPVHG8MWSXT&pf_rd_p=01d2df49-74bd-42d3-a898-95a4f3beb031'}
    
    url = URL_dict['top_kindle']
    print(f'\nURL given: {url}')

    soup = extract_soup(url)
    amz_dict = amazon_raw_crawl(soup)

    for key in amz_dict:
        print(f'{key}: {len(amz_dict[key])}')
        print(amz_dict[key])
        print('\n')
