# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os
import uuid
from math import ceil

words = [
    "聚氨酯制品 北京","地毯 北京","服装定制 北京",
    "机床维修 北京","空调维修 北京","平安护栏 北京",
    "蓄电池 北京","LED照明 北京","遮阳棚 北京",
    "古建 北京","防腐木 北京","吸音板 北京",
    "保温装饰板 北京","防水堵漏 北京","防水工程 北京",
    "电缆桥架 北京","机柜 北京","不干胶 北京",
    "空气净化 北京","隔断墙 北京","防静电地板 北京",
    "亚克力 北京","打标机 北京","氢气发生器 北京",
    "玻璃钢 北京","玻璃鳞片胶泥 北京","自动化设备 北京",
    "舞台幕布 北京","真空泵 北京","水处理 北京",
    "不锈钢水箱 北京","拆除工程 北京","灯箱制作 北京",
    "发光字 北京","发电机出租 北京","空气源热泵 北京",
    "机械加工 北京","展厅设计 北京","传感器 北京",
    "展柜货架 北京","吊车出租 北京","舞台_搭建 北京",
    "舞台灯光租赁 北京","电子白板 北京","空气净化器 北京",
    "办公家具 北京","彩钢板 北京","绿植租摆 北京",
    "波纹管 北京","软膜天花 北京","温室工程 北京",
    "泳池设备 北京","无纺布 北京","仿古瓦 北京",
    "拉弯 北京","冷库安装 北京","钢结构 北京",
    "雕塑艺术 北京","拆除公司 北京","加固公司 北京",
    "中央空调 北京","操作台 北京","无纺布袋 北京",
    "空压机 北京","软隔墙板 北京","劳保用品 北京",
    "幼儿园地板 北京","泡沫箱 北京","艾默生空调 北京",
    "艾默生UPS电源 北京","遥控门 北京","扩音器 北京",
    "仿真植物 北京","激光雕刻机 北京","风管加工 北京",
    "玻璃钢制品 北京","景观造型设计 北京","通风管道 北京",
    "香薰机 北京","电动天窗 北京","防火涂料 北京",
    "净水机 北京","过滤器 北京","钢结构 北京",
    "压缩机 北京","电子白板 北京","雕刻机 北京",
    "风幕机 北京","油烟净化 北京","宣传片制作 北京",
    "墙体彩绘 北京","净水器 北京","玻璃幕墙 北京",
    "橡胶模具 北京","监控杆 北京","园林椅 北京",
    "打卡机 北京","实木楼梯 北京","肯德基门 北京",
    "运动木地板 北京","呼叫系统 北京","eps线条 北京",
    "grc构件 北京","阳光板 北京","停车场设备 北京",
    "停车场管理 北京","弹性地板 北京","热解析仪 北京",
    "空气发生器 北京","膜结构 北京","货架 北京","墙板设备 北京",
    "立体车库 北京","机械车库 北京","古建彩绘 北京",
    "安全帽 北京","别墅门 北京","车库门 北京",
    "展厅施工 北京","加气块 北京","网上展馆 北京",
    "润滑油 北京","止水带 北京","电动卷帘门 北京",
    "装订机 北京","别墅电梯 北京","冷藏柜 北京",
    "冷藏箱 北京","太阳能路灯 北京","桑拿板 北京",
    "榻榻米 北京","变形缝 北京","美缝施工 北京","清洗机 北京",
    "表面处理 北京","铜门 北京","闸机 北京","防火门 北京",
    "展馆设计 北京","网上展馆 北京","发电机租赁 北京",
    "气候补偿器 北京","防爆机 北京","电子秤 北京",
    "印刷公司 北京","通风管道 北京","PCL 北京",
    "触摸屏 北京","断路器 北京","软启动器 北京",
    "模型公司 北京","油烟净化器 北京","卷帘门 北京",
    "绝缘材料 北京","会展服务 北京","电子沙盘 北京",
    "原木家居 北京","温室大棚 北京","岩棉板 北京",
    "仿古家具 北京","玻璃棉 北京","激光切割机 北京",
    "模具研发 北京","聚氨酯管道 北京","硅酸铝 北京",
    "汗蒸房 北京","网架 北京","logo墙制作 北京"
]

numPattern = re.compile('\d+')
def baidu(word):
    urlSearch = 'http://www.baidu.com/s'
    headers = {
        "Cookie": "BAIDUID=99F667ED27D6ABA55EFBE4720F4310D3:FG=1; BIDUPSID=99F667ED27D6ABA55EFBE4720F4310D3; PSTM=1522461331; BDUSS=3lVcWRUc3lWc0V1bGZ3RTRCcVltUXA1Qkc4MzFKLWc4OWpDUm9DQ3R-UGlaOVJiQVFBQUFBJCQAAAAAAAAAAAEAAACMBOQ5v8m~v7XEcnl5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOLarFvi2qxbY; BD_UPN=12314753; BD_HOME=1; H_PS_PSSID=26525_1465_21125_18560_28018_27245_27542; delPer=0; BD_CK_SAM=1; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=de55Hj4TWlS%2FPnolfU%2BTXc8rGSHF4V0z1WyktcVmlWytlnYh0GiM0YQX0vk; BDSVRTM=0"
    }
    params = {
        "ie": "utf-8",
        "mod": 1,
        "isbd": 1,
        "isid": "9b5f3a91000008ac",
        "f": 8,
        "rsv_bp": 1,
        "tn": "baidu",
        "wd": word,
        "oq": word,
        "rsv_pq": "9b5f3a91000008ac",
        "rsv_t": "32e5Dp4krH219FARTLAxKjqjr9zAnItiZMAc0aEHfHFdOr3xE60/dHTD9ME",
        "rqlang": "cn",
        "rsv_enter": 0,
        "bs": word,
        "rsv_sid": "undefined",
        "_ss": 1,
        "clist": "eb1081579ebe34cc	eb1081579ebe34cc	eb1081579ebe34cc",
        "hsug": "",
        "f4s": 1,
        "csor": 0,
        "_cr1": "31734"
    }
    urls = list()
    rsp = requests.get(url=urlSearch, params=params)
    soup = BeautifulSoup(rsp.text)
    numsText = soup.find(class_="nums_text")
    numsText = numsText.text.replace(',', '')
    numPatternResult = re.search(numPattern, numsText)
    nums = 0
    if numPatternResult:
        nums = ceil(int(numPatternResult.group())/15)
        if nums > 50:
            nums = 50
    for page in range(nums):
        if page != 0:
            params['pn'] = page*10
            params['rsv_page'] = page
            rsp = requests.get(url=urlSearch, params=params)
            soup = BeautifulSoup(rsp.text)
        
        index = 1
        contentLeft = soup.find(id="content_left")
        for content in contentLeft.children:
            title = content.find('h3')
            if title and title != -1:
                url = title.a['href']
                package = os.path.join('baidu', word)
                if not os.path.exists(package):
                    os.makedirs(package)
                if 'baidu.php' in url and url not in urls:
                    rspTemp = requests.get(url=url)
                    with open(os.path.join(package, f'{page+1}_{index}_v.html'), 'w', encoding="utf-8") as w:
                        w.write(rspTemp.text)
                    urls.append(url)
                    print(os.path.join(package, f'{page+1}_{index}_v.html'))
                elif 'link' in url:
                    with open('temp.html') as r:
                        template = r.read()
                    with open(os.path.join(package, f'{page+1}_{index}.html'), 'w', encoding="utf-8") as w:
                        w.write(template % (url, url))
                    print(os.path.join(package, f'{page+1}_{index}.html'))
                index = index+1


def so360(word):
    urlSearch='https://www.so.com/s'
    params={
        "q": word,
        "src": "srp",
        "fr": "none",
        "psid": "f26fe6dc9c10167f09c64b62402417d4"
    }
    rsp=requests.get(url=urlSearch,params=params)
    soup=BeautifulSoup(rsp.text)
    numsText=soup.find(class_="nums").text.replace(',','')
    numPatternResult=re.search(numPattern,numsText)
    nums = 0
    if numPatternResult:
        nums = ceil(int(numPatternResult.group())/15)
        if nums > 50:
            nums = 50
    for page in range(nums):
        if page != 0:
            params['pn'] = page
            rsp = requests.get(url=urlSearch, params=params)
            soup = BeautifulSoup(rsp.text)

        adItem = soup.find(id="e_idea_pp")
        if adItem:
            index = 1
            for content in adItem.children:
                title = content.find('a')
                if title and title != -1:
                    url = title['href']
                    package = os.path.join('360', word)
                    if not os.path.exists(package):
                        os.makedirs(package)
                    with open('temp.html') as r:
                        template = r.read()
                    with open(os.path.join(package, f'{page+1}_{index}_v.html'), 'w', encoding="utf-8") as w:
                        w.write(template % (url, url))
                    print(os.path.join(package, f'{page+1}_{index}_v.html'))
                    index = index+1
        kzItem = soup.find('ul',class_="result")
        if kzItem:
            index=1
            for content in kzItem.children:
                title = content.find('h3')
                if title and title != -1:
                    url = title.a['href']
                    package = os.path.join('360', word)
                    if not os.path.exists(package):
                        os.makedirs(package)
                    with open('temp.html') as r:
                        template = r.read()
                    with open(os.path.join(package, f'{page+1}_{index}.html'), 'w', encoding="utf-8") as w:
                        w.write(template % (url, url))
                    print(os.path.join(package, f'{page+1}_{index}.html'))
                    index = index+1
def tianyan():
    url = 'https://www.tianyancha.com/search/os1?base=bj&companyType=normal_company'
    headers = {
        "Cookie": "TYCID=54535b90dfd411e88ec1b72890c17ef8; undefined=54535b90dfd411e88ec1b72890c17ef8; ssuid=5657116243; _ga=GA1.2.1869113754.1541296303; aliyungf_tc=AQAAAAuurA0GEQkA+qUU3zIo2BYDtT/7; csrfToken=Kd-8uh-W-rlkKlDge-VamzRF; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1544336827; _gid=GA1.2.1546508247.1544336828; bannerFlag=true; token=5a76f5eb37c842468e7c63285914ac32; _utm=fe4cb4bac03e4acfa951847db8dc47b3; tyc-user-info=%257B%2522myQuestionCount%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252298%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzU1Mjc1NTM4NCIsImlhdCI6MTU0NDM0MzM0MCwiZXhwIjoxNTU5ODk1MzQwfQ.cQQyuA9ylsRpp7v1zIu0j3xO4Q-MeRWboGCZK9GBA0Kmw1RABD-TidvksUlNQlggjU1PznUqLYk9UzKBQWRHhQ%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213552755384%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzU1Mjc1NTM4NCIsImlhdCI6MTU0NDM0MzM0MCwiZXhwIjoxNTU5ODk1MzQwfQ.cQQyuA9ylsRpp7v1zIu0j3xO4Q-MeRWboGCZK9GBA0Kmw1RABD-TidvksUlNQlggjU1PznUqLYk9UzKBQWRHhQ; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1544343318",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }
    if not os.path.exists('tianyanbj.html'):
        rsp = requests.get(url=url, headers=headers)
        with open('tianyanbj.html', 'w', encoding="utf-8") as w:
            w.write(rsp.text)
        soup = BeautifulSoup(rsp.text)
    else:
        with open('tianyanbj.html', encoding="utf-8") as r:
            soup = BeautifulSoup(r.read())
    hangYe = soup.find(attrs={"tyc-event-ch": "CompanySearch.Filter.Hangye"})
    hangYe = hangYe.find(class_="content -cate")
    if not os.path.exists('tianyanbjhangye.html'):
        with open('tianyanbjhangye.html', 'w', encoding="utf-8") as w:
            for hy in hangYe.children:
                if hy.text != "全部":
                    expand = hy.find(class_="expand")
                    if expand:
                        for item in expand.children:
                            if item.text != "全部":
                                w.write(f"{item.text}@{item['href']}\n")
    else:
        with open('tianyanbjhangye.html', encoding="utf-8") as r:
            lines = r.read().split('\n')
            for line in lines:
                url = line.split('@')[-1]
                if not os.path.exists(f"hangye/pages/{url.split('?')[0].split('/')[-1]}.html") and not os.path.exists(f"hangye/page/{url.split('?')[0].split('/')[-1]}.html"):
                    hangYeRsp = requests.get(url=url, headers=headers)
                    soup = BeautifulSoup(hangYeRsp.text)
                    tipsNum = soup.find(class_="tips-num")
                    if tipsNum and int(tipsNum.text.replace('+', '')) <= 20:
                        with open(f"hangye/page/{url.split('?')[0].split('/')[-1]}.html", 'w', encoding="utf-8") as w:
                            w.write(hangYeRsp.text)
                    else:
                        with open(f"hangye/pages/{url.split('?')[0].split('/')[-1]}.html", 'w', encoding="utf-8") as w:
                            w.write(hangYeRsp.text)
    files = os.listdir('hangye/pages')
    for f in files:
        filePath = os.path.join('hangye/pages', f)
        if os.path.isfile(filePath):
            with open(filePath, encoding="utf-8") as r:
                content = r.read()
            soup = BeautifulSoup(content)
            zhuCeZiBen = soup.find(
                attrs={"tyc-event-ch": "CompanySearch.Filter.Zhuceziben"})
            ziBenItems = zhuCeZiBen.find(class_="content")
            for item in ziBenItems:
                item = item.find('a')
                if item and item != -1:
                    if item.text != '全部':
                        if not os.path.exists(os.path.join('hangye/pages', item.text)):
                            os.makedirs(os.path.join(
                                'hangye/pages', item.text, 'page'))
                            os.makedirs(os.path.join(
                                'hangye/pages', item.text, 'pages'))

                        url = item['href']
                        if not os.path.exists(os.path.join(
                                'hangye/pages', item.text, 'page', f"{url.split('?')[0].split('/')[-1]}.html")) and not os.path.exists(os.path.join(
                                'hangye/pages', item.text, 'pages', f"{url.split('?')[0].split('/')[-1]}.html")):
                            hangYeRsp = requests.get(url=url, headers=headers)
                            soup = BeautifulSoup(hangYeRsp.text)
                            tipsNum = soup.find(class_="tips-num")
                            if tipsNum and int(tipsNum.text.replace('+', '')) <= 20:
                                with open(os.path.join(
                                        'hangye/pages', item.text, 'page', f"{url.split('?')[0].split('/')[-1]}.html"), 'w', encoding="utf-8") as w:
                                    w.write(hangYeRsp.text)
                                size = os.path.getsize(os.path.join(
                                    'hangye/pages', item.text, 'page', f"{url.split('?')[0].split('/')[-1]}.html"))
                                if size <= 24541:
                                    os.remove(os.path.join(
                                        'hangye/pages', item.text, 'page', f"{url.split('?')[0].split('/')[-1]}.html"))
                                    break
                                else:
                                    print(size)
                                    print(os.path.join(
                                        'hangye/pages', item.text, 'page', f"{url.split('?')[0].split('/')[-1]}.html"))
                            else:
                                with open(os.path.join(
                                        'hangye/pages', item.text, 'pages', f"{url.split('?')[0].split('/')[-1]}.html"), 'w', encoding="utf-8") as w:
                                    w.write(hangYeRsp.text)
                                size = os.path.getsize(os.path.join(
                                    'hangye/pages', item.text, 'pages', f"{url.split('?')[0].split('/')[-1]}.html"))
                                if size <= 24541:
                                    os.remove(os.path.join(
                                        'hangye/pages', item.text, 'pages', f"{url.split('?')[0].split('/')[-1]}.html"))
                                    break
                                else:
                                    print(size)
                                    print(os.path.join(
                                        'hangye/pages', item.text, 'pages', f"{url.split('?')[0].split('/')[-1]}.html"))
            


if __name__ == '__main__':
    for word in words:
        baidu(word)
        so360(word)
        # break
    # tianyan()