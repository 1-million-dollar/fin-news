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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Economictimes News Articles
    try:
        url = 'https://economictimes.indiatimes.com/markets/stocks/news'
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # ET often changes structure, looking for common patterns
        articles = soup.select('div.eachStory') or soup.select('section#pageContent li')
        
        for item in articles[:10]:
            a_tag = item.find('a')
            if a_tag and a_tag.get('href'):
                title = a_tag.text.strip()
                if not title:
                    img = a_tag.find('img')
                    if img: title = img.get('alt', '').strip()
                
                if not title: continue
                
                article_url = a_tag.get('href')
                if not article_url.startswith('http'):
                    article_url = 'https://economictimes.indiatimes.com' + article_url
                
                news.append(title)
                link.append(article_url)
                
                img_tag = item.find('img')
                if img_tag and (img_tag.get('data-original') or img_tag.get('src')):
                    img_url.append(img_tag.get('data-original') or img_tag.get('src'))
                else:
                    img_url.append(et_logo)
    except Exception as e:
        print(f"Error fetching ET: {e}")

    # MoneyControl News Articles
    try:
        url = 'https://www.moneycontrol.com/news/business/markets/'
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        items = soup.select('li.clearfix')
        for item in items[:10]:
            a_tag = item.find('a')
            if a_tag and a_tag.get('href'):
                title = a_tag.get('title') or a_tag.text.strip()
                if not title: continue
                
                news.append(title)
                link.append(a_tag.get('href'))
                
                img_tag = item.find('img')
                if img_tag:
                    src = img_tag.get('data-src') or img_tag.get('src')
                    img_url.append(src if src else mc_logo)
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
