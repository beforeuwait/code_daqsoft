# coding=utf8

import requests
import re
import config
from lxml import etree

headers = {
    'Host': 'you.ctrip.com',
    'Referer': 'http://you.ctrip.com/sitemap/placedis/c110000',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
}

provs_url = 'http://you.ctrip.com/sitemap/placedis/c110000'

def get_provs_list():
    # 获取携程攻略里各省的列表
    # 处理直辖市，并直接放入旅游目的地列表里

    html = requests.get(provs_url, headers=headers).content.decode('utf8')
    selector = etree.HTML(html)
    prov_cons = selector.xpath('//div[@class="sitemap_toptag cf"]/li')
    text = ''
    for each in prov_cons:
        prov = each.xpath('a/text()')[0].replace('\n', '').replace(' ', '').replace('\r', '')
        url = each.xpath('a/@href')[0].replace('\n', '').replace(' ', '')
        code = re.findall('place/(.*?).html', url)[0]
        id = re.findall('\d{1,10}', code)[0]
        text += prov + config.BLANK + code + config.BLANK + id + '\n'
    with open(config.PROVS_LIST, 'a', encoding=config.ENCODING) as f:
        f.write(text)
    # 获取直辖市
    cities = selector.xpath('//div[@class="sitemap_block"]')
    data = []
    for each in cities:
        if not each.xpath('div[1]/a'):
            for i in each.xpath('ul/li'):
                city = i.xpath('a/@title')[0].replace('旅游攻略', '')
                url = i.xpath('a/@href')[0].split('/')[-1].replace('.html', '')
                data.append([city, url])
            break
    text = ''
    all_citys = [i.strip().split(config.BLANK) for i in open(config.ALL_CITY_LIST, 'r', encoding=config.ENCODING)]
    for i in data:
        for t in all_citys:
            if i[0] in t:
                text += config.BLANK.join(t).replace('&', '') + config.BLANK + i[1] + '\n'
                break
    with open(config.CITY_LIST, 'a', encoding=config.ENCODING) as f:
        f.write(text)

def get_city_list():
    prov_list = [i.strip().split('\u0001') for i in open(config.PROVS_LIST, 'r', encoding='utf8')]
    all_citys = [i.strip().split(config.BLANK) for i in open(config.ALL_CITY_LIST, 'r', encoding=config.ENCODING)]
    data = []
    for each in prov_list:
        print(each)
        url = 'http://you.ctrip.com/sitemap/place/c%s' % each[2]
        html = requests.get(url, headers=headers, proxies=config.get_proxy()).content.decode('utf8')
        selector = etree.HTML(html)
        cons = selector.xpath('//div[@class="sitemap_block"]/ul[1]/li')
        for i in cons:
            city = i.xpath('a/text()')[0].replace('旅游攻略', '')
            url = i.xpath('a/@href')[0].split('/')[-1].replace('.html', '')
            data.append([each[0], city, url])

    text = ''
    for i in data:
        for t in all_citys:
            if i[0] in t and i[1] in t:
                count = t.index(i[1])
                if count == 2 or count == 3:
                    t[4], t[5] = '', ''
                    t[-1] = str(re.findall('\d\d\d\d', t[-1])[0]) + '00'
                    text += config.BLANK.join(t) + config.BLANK + i[-1] + '\n'
                else:
                    text += config.BLANK.join(t) + config.BLANK + i[-1] + '\n'
                break

    with open(config.CITY_LIST, 'a', encoding=config.ENCODING) as f:
        f.write(text)

def get_sub_area():
    city_list = [i.strip().split(config.BLANK)for i in open(config.CITY_LIST, 'r', encoding=config.ENCODING)]
    data = []
    for each in city_list:
        print(each)
        if not each[4] == '':
            each.append('')
            data.append(each)
        else:
            data.extend(get_sub_area_logic(each))

    # 再次匹配内容
    for each in data:
        for t in (i.strip().split(config.BLANK)for i in open(config.ALL_CITY_LIST, 'r', encoding=config.ENCODING)):
            if each[0] in t and each[2] in t and each[5] in t and each[4] == '':
                each[5] = t[5]
                each[6] = t[6]
    content = ''
    # 写入文件
    for each in data:
        each[4], each[5] = each[5], each[4]
        content += config.BLANK.join(each) + '\n'
    with open(config.CITY_LIST, 'w', encoding=config.ENCODING) as f:
        f.write(content)

def get_sub_area_logic(each):
    data = []
    url = 'http://you.ctrip.com/restaurantlist/%s.html' %each[-1]
    retry = 5
    html = ''
    while retry > 0:
        try:
            html = requests.get(url, headers=headers, proxies=config.get_proxy()).content.decode(config.ENCODING)
            break
        except:
            pass
        retry -= 1
    selector = etree.HTML(html)
    cons = selector.xpath('//div[@id="locationDiv"]/p/a')
    for i in cons:
        info = each.copy()
        area = i.xpath('text()')[0] if i.xpath('text()') else ''
        co = i.xpath('@onclick')[0] if i.xpath('@onclick') else ''
        code = re.findall('OnRegion\((.*?)\)', co)[0]
        info[5] = area
        info.append(code)
        data.append(info)
    return data

def execute():
    # 每次抓取列表前，首先要清空文件
    f = open(config.PROVS_LIST, 'w+', encoding=config.ENCODING)
    g = open(config.CITY_LIST, 'w+', encoding=config.ENCODING)
    f.close()
    g.close()
    get_provs_list()
    get_city_list()
    get_sub_area()

if __name__ == '__main__':
    execute()