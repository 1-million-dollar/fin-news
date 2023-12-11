from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

news = []
link = []
img_url = []

# logos
et_logo = 'https://economictimes.indiatimes.com/photo/msid-74451948,quality-100/et-logo.jpg'
mc_logo = 'https://images.moneycontrol.com/images/common/header/logo_105x22.png?impolicy=mchigh'

# Economictimes News Articles
url = 'https://economictimes.indiatimes.com/markets'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

u_list = soup.find('ul', class_="newsList")
list = u_list.find_all('li')
for item in list:
    if item != None:
        a_tag = item.find('a')
        if a_tag != None:
            news.append(a_tag.text)
            article_url = url + a_tag.get('href')
            link.append(article_url)
            page = requests.get(article_url)
            soup = BeautifulSoup(page.text, 'html.parser')
            article_image_fig = soup.find('figure', class_ = "artImg")
            if article_image_fig != None:
              img_url.append(article_image_fig.find('img').get('src'))
            else: 
              img_url.append(et_logo)
# MoneyControl News Articles
url = 'https://www.moneycontrol.com/news/business/markets/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

u_list = soup.find('ul', id="cagetory")
list = u_list.find_all('li')
for item in list:
  if item != None:
      heading_tag = item.find('h2')

  if heading_tag != None:
      a_tag = heading_tag.find('a')
      news.append(a_tag.text)
      link.append(a_tag.get('href'))
      page = requests.get(a_tag.get('href'), allow_redirects=False)
      soup = BeautifulSoup(page.text, 'html.parser')
      article_image_div = soup.find('div', class_ = "article_image")
      if article_image_div != None:
        img_url.append(article_image_div.find('img').get('data-src'))
      else:
        img_url.append(mc_logo)
        


@app.route('/')
def hello_world(news=news, link=link,img_url=img_url, l=len(news)):
  return render_template('home.html', news=news, link=link,img_url=img_url, l=l)


if __name__ == '__main__':
  app.run(host= '0.0.0.0', debug=True)