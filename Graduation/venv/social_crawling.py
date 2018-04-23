from bs4 import BeautifulSoup

# 쿠팡 크롤링 함수
def crawling_coupang_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    notice = soup.find_all('div', {"class": "sdp-review__article__list__review__content js_reviewArticleContent"})
    return notice

def crawling_tmon_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    notice = soup.find_all('div', {"class": "sdp-review__article__list__review__content js_reviewArticleContent"})
    return notice