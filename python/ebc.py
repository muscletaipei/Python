import requests
import time
from newspaper import Article
from bs4 import BeautifulSoup
import csv


def get_news_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    hrefs = soup.find_all('div', 'style1 white-box')
    for href in hrefs:
        print(href.find('a')['href'])
        url_list.append(href.find('a')['href'])

    days = soup.find_all('span', 'small-gray-text')
    for day in days:
        if day.text != '':
            all_date.append(day.text)
            print(day.text)


def get_content(url_list):
    for i in range(len(url_list)):
        url = 'https://news.ebc.net.tw' + url_list[i]
        content = Article(url, language='zh')  # Chinese

        try:
            content.download()
            content.parse()

            print(url)

            all_url.append(url)
            all_title.append(content.title)
            print(content.title)

            process_text(content.text)
            time.sleep(5)
        except:
            print(url)
            print("網址錯誤無日期")

            all_url.append(url)
            all_date.append("網址錯誤無日期")

            all_title.append("網址錯誤無標題")
            print("網址錯誤無標題")

            process_text("網址錯誤無內文")
            time.sleep(2)


def process_text(ori_text):
    content_list = []
    index_list = []
    content_list = ori_text.split('\n\n')

    for i in range(len(content_list)):
        if content_list[i].find('熱門點閱') != -1 or content_list[i].find('好文推薦') != -1 or content_list[i].find('►') != -1 or content_list[i].find('●') != -1 or content_list[i].find('★') != -1 or content_list[i].find('▲') != -1 or (content_list[i].find('／') != -1 and content_list[i].find('報導') != -1):
            index_list.append(i)
    remove_content(content_list, index_list)


def remove_content(content_list, index_list):
    for i in range(len(index_list)):
        del content_list[index_list[i]-i]
    keyword_count = 0
    keyword_list = ['多元成家', '婚姻平權', '同性婚姻', '同婚', '同性伴侶', '伴侶盟',
                    '伴侶權益推動', '伴侶制度', '同性戀', '異性戀', '同志', '守護家庭', '護家盟', '一夫一妻']
    for i in range(len(content_list)):
        for j in range(len(keyword_list)):
            keyword_count += content_list[i].count(keyword_list[j])

    if keyword_count >= 3:
        all_content.append(content_list)
        print(content_list)
    else:
        all_content.append("內容不符合keyword or 網址錯誤")
        print("內容不符合keyword or 網址錯誤" + str(content_list))


def write_to_csv():
    with open('東森-多元成家.csv', 'w', encoding='utf-8_sig', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['新聞標題', '文章內容', '超連結', '發佈時間'])
        for i in range(len(all_content)):
            writer.writerow(
                [all_title[i], all_content[i], all_url[i], all_date[i]])


if __name__ == '__main__':
    all_content = []
    all_url = []
    all_date = []
    all_title = []
    for j in range(1, 2):
        url_list = []
        url = 'https://news.ebc.net.tw/Search/Result?type=keyword&value=%25E5%25A4%259A%25E5%2585%2583%25E6%2588%2590%25E5%25AE%25B6&page=' + \
            str(j)
        get_news_url(url)
        get_content(url_list)
    write_to_csv()
