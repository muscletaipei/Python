import requests
import time
from newspaper import Article
from bs4 import BeautifulSoup
import csv


def get_news_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    hrefs = soup.find_all('a', 'tit')
    try:
        for href in hrefs:
            print(href['href'])
            url_list.append(href['href'])

        searchlist = soup.find('ul', 'list boxTitle')
        days = searchlist.find_all('span')
        for day in days:
            if day.text != '':
                all_date.append(day.text)
                print(day.text)
    except:
        print('查無新聞！！')
        time.sleep(1)


def get_content(url_list):
    for i in range(len(url_list)):
        url = url_list[i]
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
        if content_list[i].find('熱門點閱') != -1 or content_list[i].find('／') != -1 or content_list[i].find('好文推薦') != -1 or content_list[i].find('►') != -1 or content_list[i].find('●') != -1 or content_list[i].find('▼') != -1 or content_list[i].find('★') != -1 or content_list[i].find('▲') != -1 or content_list[i].find('圖／') != -1 or (content_list[i].find('／') != -1 and content_list[i].find('報導') != -1):
            index_list.append(i)
    remove_content(content_list, index_list)


def remove_content(content_list, index_list):
    for i in range(len(index_list)):
        del content_list[index_list[i]-i]
    keyword_count = 0
    keyword_list = ['台積電']
    for i in range(len(content_list)):
        for j in range(len(keyword_list)):
            keyword_count += content_list[i].count(keyword_list[j])
    if keyword_count >= 1:
        all_content.append(content_list)
        print(content_list)
    else:
        all_content.append("內容不符合keyword or 網址錯誤")
        print("內容不符合keyword or 網址錯誤")


def savefile(beginday, stopday, news):
    filename = 'cnyes-'+beginday+'~'+stopday+'.csv'
    with open(filename, 'a', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(news)


def write_to_csv():
    with open('ltn.csv', 'w', encoding='utf-8_sig', newline="") as csvfile:
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
    start_time = ['20211220']
    end_time = ['20211231']

    for k in range(len(start_time)):
        time_url = 'https://search.ltn.com.tw/list?keyword=%E5%8F%B0%E7%A9%8D%E9%9B%BB&conditions=and&start_time=' + \
            start_time[k] + '&end_time=' + end_time[k]
        print(time_url)
        html = requests.get(time_url).text
        soup = BeautifulSoup(html, 'html.parser')

        try:
            last_page = soup.find('a', 'p_last')['href']
            the_last_page = int(last_page[-1])
        except:
            the_last_page = 1

        for j in range(1, the_last_page + 2):
            url_list = []
            url = time_url + '&page=' + str(j)
            print('\n------------------------\n')
            print('正在獲取第' + str(j) + '頁')
            print('\n------------------------\n')
            get_news_url(url)
            get_content(url_list)
    write_to_csv()
