# import module

import requests
import argparse
import pandas as pd
from bs4 import BeautifulSoup

def getdata(url):
  '''
  Description: Fetches the content of a given URL.

  Input: url (str): The URL to fetch.

  Output: The content of the URL
  '''
  r = requests.get(url)
  return r.text
def get_soup(url):

  '''
  Description: Fetches the HTML content of a given URL and parses it using BeautifulSoup.

  Input: url (str): The URL to fetch.

  Output: The parsed HTML content.
  '''
  htmldata = getdata(url)
  soup = BeautifulSoup(htmldata, 'html.parser')
  return (soup)

def get_review_body(soup):
  '''
  Description: Extracts review bodies from a BeautifulSoup object.

  Input:soup (BeautifulSoup): The parsed HTML content.

  Output: list: A list of review body strings.
  '''
  data_str = ""
  review_body = []
  for item in soup.find_all("span", class_="a-size-base review-text"):
    data_str = data_str + item.get_text()
    review_body.append(data_str)
    data_str = ""
  return review_body

def get_review_title_rating(soup):
  '''
  Description: Extracts review titles and ratings from a BeautifulSoup object.
  Input: soup (BeautifulSoup): The parsed HTML content.
  Output: A list of review_titles that review titles and a list of ratings that spcifices ratings.
  '''
  data_str = ""
  review_title = []
  rating=[]
  for item in soup.find_all("a", class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"):
    data_str = data_str + item.get_text()
    parts = data_str.strip().split("\n")
    rating.append(parts[0])
    review_title.append(parts[1])
    data_str = ""
  return review_title, rating

def get_verified(soup):
  '''
  Description: Extracts verification status from a BeautifulSoup object.

  Input: soup (BeautifulSoup): The parsed HTML content.

  Output: list: A list of verification statuses.
  '''
  data_str = ""
  verified = []
  for item in soup.find_all("span", class_="a-size-mini a-color-state a-text-bold"):
    data_str = data_str + item.get_text()
    verified.append(data_str)
    data_str = ""
  return verified

def get_color_and_size(soup):
  '''
  Description: Extracts color and size information from a BeautifulSoup object.

  Input: soup (BeautifulSoup): The parsed HTML content.

  Output:color_list that spicifies color and size_list that specifies size.

  '''
  color_list = []
  size_list=[]

  # Find the specific div by ID
  review_card = soup.find('div',class_="card-padding" )  #id="R26M9UAW45Z9CP-review-card"

  # If the review card is found, extract color information
  if review_card:
    sub_card=review_card.find('div',class_="a-row a-spacing-mini review-data review-format-strip")
    for div in review_card.find_all('div', class_="a-row a-spacing-mini review-data review-format-strip"):
          color_span = div.find('span', class_="a-color-secondary")
          if color_span:
              text = color_span.get_text().strip()
              if text.lower().startswith('colour'):
                color = 'NA'
                size = 'NA'
                # Find the index of 'Size:'
                color_key_index=text.find('Colour:')
                size_index = text.find('Size:')
                pattern_index=text.find('Pattern Name:')
                # If 'Size:' is found, extract the size and color
                if size_index != -1:
                    size = text[size_index:pattern_index].split(':')[1].strip()
                    color = text[color_key_index+7:size_index].strip()
                    color_list.append(color)
                    size_list.append(size)
          else:
              color_list.append('NA')
              size_list.append('NA')

  return color_list,size_list


def main():
  '''
  Description: This Python code defines a function main() that scrapes reviews from an Amazon product page and saves them to a CSV file (amazon_review.csv).

  Input:L: The url specifies the URL of the Amazon product page to scrape reviews from.

  Output:A CSV file named amazon_review.csv is created with the scraped review data.

  '''
  try:
    parser = argparse.ArgumentParser(description="Scrape Amazon reviews")
    parser.add_argument("url",
                        help="URL of the Amazon product page (default: iPhone 12)")
    args = parser.parse_args()

    url = args.url
    # url = "https://www.amazon.in/Apple-iPhone-Pro-Max-256/dp/B0CHWWW471/ref=pd_rhf_dp_s_pd_sbs_rvi_d_sccl_1_6/258-0341900-8181736?pd_rd_w=mMh75&content-id=amzn1.sym.ed04a9b6-f1e8-467f-8e81-e050db1b5151&pf_rd_p=ed04a9b6-f1e8-467f-8e81-e050db1b5151&pf_rd_r=08GDXN4T8SZJQFVV12VS&pd_rd_wg=1QEqP&pd_rd_r=540b3b93-dccb-4a68-b934-24b1c959d11d&pd_rd_i=B0CHWWW471&th=1"
    soup = get_soup(url)
    print('Scrapped Web data Successfully')

    review_body = get_review_body(soup)

    review_title,rating = get_review_title_rating(soup)
    # rating = get_rating(soup)
    verified = get_verified(soup)
    color,size = get_color_and_size(soup)
    data_array=[]
    for i in range(len(review_title)):
      data_array.append([review_title[i],review_body[i],verified[i],color[i],size[i],rating[i]])

    dataframe= pd.DataFrame(data_array,columns=['Review_Title','Review Body','Verified','Color','Size','Rating'])

    dataframe.to_csv('amazon_review.csv')
    print('Creaetd Dataframe of scrapped data Successfully')
  except Exception as err:
    print('Exception occured: ', err)


if __name__=='__main__':
  main()


