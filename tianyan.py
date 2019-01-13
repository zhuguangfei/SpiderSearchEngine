# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os
import uuid
from math import ceil


def tianyan(companyName):
    url = 'https://www.qichacha.com/search'
    data = {"key": "北京英策长远电子科技有限公司"}
    headers = {
        "Cookie": "UM_distinctid=16783d942c2330-09ff793d972d07-3961430f-100200-16783d942c3250; zg_did=%7B%22did%22%3A%20%2216783d942e755-086111bb199ba2-3961430f-100200-16783d942e82ff%22%7D; _uab_collina=154410531352807114503515; saveFpTip=true; QCCSESSID=37pckqk9j0udc3oagpo9msia12; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1546739420,1546770883,1546781934,1547348166; acw_tc=7cc1e21a15473481549781056ebbfcff9283342f0b85f2a706b0bc12b6; CNZZDATA1254842228=822079952-1544102708-https%253A%252F%252Fwww.baidu.com%252F%7C1547392611; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201547390342389%2C%22updated%22%3A%201547393069464%2C%22info%22%3A%201547348166270%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22013ba066be258684c32dec669e8d9182%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1547393070",
        # User-Agent: "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }
    proxies = {
        "http": "http://114.106.151.183:9999"
    }
    rsp = requests.get(url=url, headers=headers, params=data, proxies=proxies)
    with open('a.html', 'w', encoding="utf-8") as w:
        w.write(rsp.text)
    soup = BeautifulSoup(rsp.text)
    table = soup.find('table', class_="m_srchList")
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        print(tds)
        companyInfo = tds[1]
        print(companyInfo.a.text)
        ps = companyInfo.find_all('p')
        if len(ps) > 0:
            print(ps[0].a.text)
            print(ps[1].span.a.text)
        # print(tds[2].text)
        # break


if __name__ == '__main__':
    tianyan('')

# import tkinter
# from tkinter import Label, Button, Entry
# root = tkinter.Tk()
# root.geometry("450x90")
# root.title('搜索引擎爬虫工具')
# labelWord = Label(text='关键词')
# textWord = Entry()
# labelWord.grid(row=2, column=2)
# textWord.grid(row=2, column=3)
# labelStartPage = Label(text='起始页')
# textStartPage = Entry()
# labelEndPage = Label(text='终止页')
# textEndPage = Entry()
# labelStartPage.grid(row=3, column=2)
# textStartPage.grid(row=3, column=3)
# labelEndPage.grid(row=3, column=5)
# textEndPage.grid(row=3, column=6)


# def crawl():
#     word = textWord.get()
#     start = textStartPage.get()
#     end = textEndPage.get()
#     # baidu(word, int(start), int(end))
#     baiduPage(word, int(start), int(end))


# empty = Label(text='    ')
# submit = Button(text='启动', command=crawl)
# empty.grid(row=4, column=1)
# submit.grid(row=4, column=2)
# root.mainloop()
