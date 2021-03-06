'''作为配置文件的存在'''

import os

os.chdir(os.path.split(os.path.realpath(__file__))[0])

# 命令
RESTAURANT_COMMAND = 'cmt'

SHOPPING_COMMAND = 'cmt'

# 因为评论不做天更新的，因此，评论获取指定的一段时间内的全部评论
# 新逻辑中，被弃用
CMT_START_DATE = '2012-01-01'
CMT_START_END = '2017-10-25'



PATH = 'Data'
if not os.path.exists(PATH):
    os.mkdir(os.path.abspath(PATH))

TEMP = 'DataTemp'
if not os.path.exists(TEMP):
    os.mkdir(os.path.abspath(TEMP))

LIST = 'DataList'
if not os.path.exists(LIST):
    os.mkdir(os.path.abspath(LIST))

ALL_CITY_LIST = os.path.join(os.path.abspath(LIST), 'city_list_total.txt')

SHOP_CMT_START = os.path.join(os.path.abspath(LIST), 'start_date_shop.txt')
SHOP_CMT_END = os.path.join(os.path.abspath(LIST), 'end_date_shop.txt')

RESTAURANT_CMT_START = os.path.join(os.path.abspath(LIST), 'start_date_food.txt')
RESTAURANT_CMT_END = os.path.join(os.path.abspath(LIST), 'end_date_food.txt')

#

CITY_LIST = os.path.join(os.path.abspath(LIST), 'city_list.txt')    # 城市列表
if not os.path.exists(CITY_LIST):
    f = open(CITY_LIST, 'w+')
    f.close()

PROVS_LIST = os.path.join(os.path.abspath(TEMP), 'provs_list.txt')  # 临时的省份列表
if not os.path.exists(PROVS_LIST):
    f = open(PROVS_LIST, 'w+')
    f.close()

# 餐馆

RESTAURANT_SHOP_LIST = os.path.join(os.path.abspath(PATH), 'restaurant_shop_list.txt')
if not os.path.exists(RESTAURANT_SHOP_LIST):
    f = open(RESTAURANT_SHOP_LIST, 'w+')
    f.close()

RESTAURANT_SHOP_INFO = os.path.join(os.path.abspath(PATH), 'restaurant_shop_info.txt')
if not os.path.exists(RESTAURANT_SHOP_INFO):
    f = open(RESTAURANT_SHOP_INFO, 'w+')
    f.close()


RESTAURANT_SHOP_EX = os.path.join(os.path.abspath(PATH), 'restaurant_shop_ex.txt')  # 记录已抓取目录已经pid
if not os.path.exists(RESTAURANT_SHOP_EX):
    f = open(RESTAURANT_SHOP_EX, 'w+')
    f.close()

RESTAURANT_SHOP_CMT = os.path.join(os.path.abspath(PATH), 'restaurant_shop_cmt_%s_%s.txt')
# if not os.path.exists(RESTAURANT_SHOP_CMT):
#     f = open(RESTAURANT_SHOP_CMT, 'w+')
#     f.close()

RESTAURANT_CMT_DONE = os.path.join(os.path.abspath(PATH), 'restaurant_cmt_done.txt')
if not os.path.exists(RESTAURANT_CMT_DONE):
    f = open(RESTAURANT_CMT_DONE, 'w+')
    f.close()

# 商铺购物
SHOPPING_SHOP_LIST= os.path.join(os.path.abspath(PATH), 'shopping_shop_list.txt')
if not os.path.exists(SHOPPING_SHOP_LIST):
    f = open(SHOPPING_SHOP_LIST, 'w+')
    f.close()

SHOPPING_SHOP_INFO = os.path.join(os.path.abspath(PATH), 'shopping_shop_info.txt')
if not os.path.exists(SHOPPING_SHOP_INFO):
    f = open(SHOPPING_SHOP_INFO, 'w+')
    f.close()

SHOPPING_SHOP_EX = os.path.join(PATH, 'shopping_shop_ex.txt')
if not os.path.exists(SHOPPING_SHOP_EX):
    f = open(SHOPPING_SHOP_EX, 'w+')
    f.close()

SHOPPING_SHOP_LIST_EX = os.path.join(os.path.abspath(PATH), 'shopping_shop_list_ex.txt')
if not os.path.exists(SHOPPING_SHOP_LIST_EX):
    f = open(SHOPPING_SHOP_LIST_EX, 'w+')
    f.close()

SHOPPING_SHOP_CMT = os.path.join(os.path.abspath(PATH), 'shopping_shop_cmt_%s_%s.txt')
# if not os.path.exists(SHOPPING_SHOP_CMT):
#     f = open(SHOPPING_SHOP_CMT, 'w+')
#     f.close()

SHOPPING_CMT_DONE = os.path.join(os.path.abspath(PATH), 'shopping_cmt_done.txt')
if not os.path.exists(SHOPPING_CMT_DONE):
    f = open(SHOPPING_CMT_DONE, 'w+')
    f.close()


# 代理
PROXY = {
    "http": "http://HY3JE71Z6CDS782P:CE68530DAD880F3B@proxy.abuyun.com:9010",
    "https": "http://HY3JE71Z6CDS782P:CE68530DAD880F3B@proxy.abuyun.com:9010",
}

# 编码
BLANK = '\u0001'
ENCODING = 'utf-8'

# 请求头
HEADERS = {
    "Host": "you.ctrip.com",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}
HEADERS_XML = {
    "X-Requested-With": "XMLHttpRequest",
    "Host": "you.ctrip.com",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

RESTAURANT_DATA = {
    "poiID": "11383200",
    # "districtId": "104",
    "districtEName": "Chengdu",
    "pagenow": 1,
    "order": 1,
    "star": 0,
    "tourist": 0,
    "resourceId": "5233332",
    "resourcetype": 3,
}

SHOPPING_DATA = {
    "poiID": "10566545",
    "districtId": "104",
    "districtEName": "Chengdu",
    "pagenow": 1,
    "order": 1,
    "star": 0,
    "tourist": 0,
    "resourceId": "138472",
    "resourcetype": 4,
}

# 字段，类似scrapy里的item

RESTAURANT_DICT = {
    "中文全称": "",
    "中文简称": "",
    "所属地区": "",
    "地址": "",
    "地理位置": "",
    "类型": "",
    "等级": "",
    "营业时间": "",
    "人均消费": "",
    "特色菜品": "",
    "咨询电话": "",
    "传真": "",
    "邮政编码": "",
    "投诉电话": "",
    "交通信息": "",
    "周边信息": "",
    "简介": "",
    "国别": "CN",
    "省自治区全称": "",
    "省自治区简称": "",
    "市州全称": "",
    "市州简称": "",
    "区县全称": "",
    "区县简称": "",
    "地区编码": "",
    "url": "",
}
RESTAURANT_DICT_L = [
    "中文全称", "中文简称", "所属地区", "地址", "地理位置", "类型", "等级", "营业时间", "人均消费",
    "特色菜品", "咨询电话", "传真", "邮政编码", "投诉电话", "交通信息", "周边信息", "简介", "国别",
    "省自治区全称", "省自治区简称", "市州全称", "市州简称", "区县全称", "区县简称", "地区编码", "url"
]


SHOPPING_DICT = {
    "中文全称": "",
    "中文简称": "",
    "所属地区": "",
    "地址": "",
    "地理位置": "",
    "类型": "",
    "营业时间": "",
    "特色商品": "",
    "传真": "",
    "邮政编码": "",
    "投诉电话": "",
    "交通信息": "",
    "周边信息": "",
    "简介": "",
    "国别": "CN",
    "省自治区全称": "",
    "省自治区简称": "",
    "市州全称": "",
    "市州简称": "",
    "区县全称": "",
    "区县简称": "",
    "地区编码": "",
    "url": "",
}

SHOPPING_DICT_L = [
    "中文全称", "中文简称", "所属地区", "地址", "地理位置", "类型", "营业时间", "特色商品", "传真", "邮政编码", "投诉电话",
    "交通信息", "周边信息", "简介", "国别", "省自治区全称", "省自治区简称", "市州全称", "市州简称",
    "区县全称", "区县简称", "地区编码", "url",
]

HDFS_PATH = '/user/spider/bianmu_22_data/%s'