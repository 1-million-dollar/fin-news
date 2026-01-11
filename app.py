from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# logos
et_logo = 'https://economictimes.indiatimes.com/photo/msid-74451948,quality-100/et-logo.jpg'
mc_logo = 'https://images.moneycontrol.com/images/common/header/logo_105x22.png?impolicy=mchigh'

def get_news():
    news = []
    link = []
    img_url = []

    # Economictimes News Articles
    try:
        url = 'https://economictimes.indiatimes.com/markets'
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        u_list = soup.find('ul', class_="newsList")
        if u_list:
            items = u_list.find_all('li')
            for item in items[:10]: # Limit to first 10 for speed
                a_tag = item.find('a')
                if a_tag and a_tag.get('href'):
                    title = a_tag.text.strip()
                    article_url = a_tag.get('href')
                    if not article_url.startswith('http'):
                        article_url = 'https://economictimes.indiatimes.com' + article_url
                    
                    news.append(title)
                    link.append(article_url)
                    
                    # Try to get article image
                    try:
                        art_page = requests.get(article_url, headers=headers, timeout=5)
                        art_soup = BeautifulSoup(art_page.text, 'html.parser')
                        img_tag = art_soup.find('img', class_="img-responsive") or art_soup.find('figure', class_="artImg")
                        if img_tag:
                            src = img_tag.get('src') if img_tag.name == 'img' else img_tag.find('img').get('src')
                            img_url.append(src)
                        else:
                            img_url.append(et_logo)
                    except:
                        img_url.append(et_logo)
    except Exception as e:
        print(f"Error fetching ET: {e}")

    # MoneyControl News Articles
    try:
        url = 'https://www.moneycontrol.com/news/business/markets/'
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        u_list = soup.find('ul', id="cagetory")
        if u_list:
            items = u_list.find_all('li')
            for item in items[:10]:
                heading = item.find('h2')
                if heading:
                    a_tag = heading.find('a')
                    if a_tag and a_tag.get('href'):
                        news.append(a_tag.text.strip())
                        link.append(a_tag.get('href'))
                        
                        img_tag = item.find('img')
                        if img_tag and img_tag.get('data-src'):
                            img_url.append(img_tag.get('data-src'))
                        elif img_tag and img_tag.get('src'):
                            img_url.append(img_tag.get('src'))
                        else:
                            img_url.append(mc_logo)
    except Exception as e:
        print(f"Error fetching MC: {e}")

    return news, link, img_url

@app.route('/')
def hello_world():
    news_list, links, imgs = get_news()
    return render_template('home.html', news=news_list, link=links, img_url=imgs, l=len(news_list))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
