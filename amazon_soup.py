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

    return soup_dict

def top_amazon_boxes(soup):
    boxes = soup.find_all('div', attrs={'class':"a-section a-spacing-none aok-relative"})

    return boxes

def boxes_info(boxes):
    
    ranks = []
    # product_names = []
    # image_urls = []
    star_ratings = []
    reviews = []
    authors_companies = []
    editions_consoles = []

    amz_mx_url = 'https://www.amazon.com.mx'

    for box in boxes:
        rank_box = box.find_all('span', attrs={'class':'zg-badge-text'})
        # products_and_image_box = box.find_all('div', attrs={'class' : 'a-section a-spacing-small'})
        star_ratings_box = box.find_all('span', attrs={'class' : 'a-icon-alt'})
        reviews_box = box.find_all('a', attrs={'class' : 'a-size-small a-link-normal'})
        authors_company_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-base'})
        editions_console_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-secondary'})
        
        rank = rank_box[0].get_text()
        # product_names = product_name.img.get('alt') for product_name in products_and_image]
        # image_urls = [image_url.img.get('src') for image_url in products_and_image]
        try:
            star_rating = star_ratings_box[0].get_text()
            review = reviews_box[0].get_text()
            author_company = authors_company_box[0].get_text()
            edition_console = editions_console_box[0].get_text()
        except:
            star_rating = 'N/A'
            review = 'N/A'
            author_company = 'N/A'
            edition_console = 'N/A'
            print(star_ratings_box)

        ranks.append(rank)
        # product_names.append(product_name)
        # image_urls.append(image_url)
        star_ratings.append(star_rating)
        reviews.append(review)
        authors_companies.append(author_company)
        editions_consoles.append(edition_console)

    # print(ranks)
    boxes_dict = {"Rank" : ranks,
    "Stars": star_ratings,
    "Reviews": reviews,
    "Authors/Company": authors_companies,
    "Edition/Console": editions_consoles
    }

    # "Product Names": product_names, 
    # "Image urls": image_urls,


    return boxes_dict

if __name__=='__main__':

    URL_dict = {'AMZ_Mex' : 'https://www.amazon.com.mx/',
            'top_kindle' : 'https://www.amazon.com.mx/gp/bestsellers/digital-text/ref=zg_bs_digital-text_home_all?pf_rd_p=01d2df49-74bd-42d3-a898-95a4f3beb031&pf_rd_s=center-4&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=6APAMAKKFSPVHG8MWSXT&pf_rd_r=6APAMAKKFSPVHG8MWSXT&pf_rd_p=01d2df49-74bd-42d3-a898-95a4f3beb031',
            'top_dep_al' : 'https://www.amazon.com.mx/gp/bestsellers/sports/ref=zg_bs_sports_home_all?pf_rd_p=c94501c9-6cef-4a3b-b0bb-7746f3943c94&pf_rd_s=center-2&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_p=c94501c9-6cef-4a3b-b0bb-7746f3943c94',
            'top_salud' : 'https://www.amazon.com.mx/gp/bestsellers/hpc/ref=zg_bs_hpc_home_all?pf_rd_p=e97d3657-a6f5-4f7d-b4cb-9fadc7d4db08&pf_rd_s=center-3&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_p=e97d3657-a6f5-4f7d-b4cb-9fadc7d4db08',
            'top_videojuegos': 'https://www.amazon.com.mx/gp/bestsellers/videogames/ref=zg_bs_videogames_home_all?pf_rd_p=5ed465af-ad52-4ddb-ad7c-8f0f329c8097&pf_rd_s=center-4&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_p=5ed465af-ad52-4ddb-ad7c-8f0f329c8097',
            'top_hogar': 'https://www.amazon.com.mx/gp/bestsellers/kitchen/ref=zg_bs_kitchen_home_all?pf_rd_p=75c4db55-6e8d-4e66-81e4-028eeccd0f00&pf_rd_s=center-5&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_p=75c4db55-6e8d-4e66-81e4-028eeccd0f00',
            'top_bebe': 'https://www.amazon.com.mx/gp/bestsellers/baby/ref=zg_bs_baby_home_all?pf_rd_p=41cc0369-7172-4c59-935b-1390de9c35cb&pf_rd_s=center-6&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_p=41cc0369-7172-4c59-935b-1390de9c35cb',
            'top_libros':'https://www.amazon.com.mx/gp/bestsellers/books/ref=zg_bs_books_home_all?pf_rd_p=d621d82d-2b96-4fd0-a6e9-2011b2578fa1&pf_rd_s=center-1&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_r=JC0QADQBXQSN2CPQTN1V&pf_rd_p=d621d82d-2b96-4fd0-a6e9-2011b2578fa1'}
    
    url = URL_dict['top_kindle']
    print(f'\nURL given: {url}')

    soup = extract_soup(url)
    # amz_dict = amazon_raw_crawl(soup)

    boxes = top_amazon_boxes(soup)
    print(f'Boxes: {len(boxes)}')
    amaz_dict2 = boxes_info(boxes)

    # for key in amz_dict:
    #     print(f'{key}: {len(amz_dict[key])}')
    #     print(amz_dict[key])
    #     print('\n')

    for key in amaz_dict2:
        print(f'{key}: {len(amaz_dict2[key])}')
        print(amaz_dict2[key])
        print('\n')

