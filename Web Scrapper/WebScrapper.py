import requests
from bs4 import BeautifulSoup
def extract_news_headlines(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    NEWS = soup.find_all("div", class_="news_Itm")
    # print(NEWS)
    for i in NEWS:
        if NEWS:
            news_items = i.find("h2", class_="newsHdng")
            # print(news_items)
            if news_items:
                a_tag = news_items.find("a")
                if a_tag:
                    link = a_tag.get("href")
                    txt = a_tag.text.strip()
                    headlines.append((txt, link))
    return headlines


url = "https://www.ndtv.com/latest#pfrom=home-ndtv_main"
h = extract_news_headlines(url)


for i, news in enumerate(h):
    print(f"{i+1}. {news[0]}\n🔗: {news[1]}\n\n")
