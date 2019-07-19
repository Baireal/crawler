# -*-coding:utf-8 -*-
# 添加filter=0，之后使用下一页的方式，只修改了pn（也许可以不修改）；7页之后人机验证
import requests, os
import urllib, xlwt
import re,time,random
from lxml import etree
import warnings,coinaddr
#添加直接验证地址 coinaddr
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#直接由start=xx请求网页，搜索一次后（33页）出现人机验证

user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        # iPhone 6：
        "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]

'''
#浏览器不同，xpath不同
headers = {
        'user-agent': random.choice(user_agent) ,
        'connection': "close",  # keep-alive
    }'''
headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'connection': "close",
    }


#验证地址是否为比特币地址
def verify(addr):
    try:
        result = coinaddr.validate('btc', addr)
        # print(result)
        if 'valid=True' in str(result):
            return 1
        else:
            return 0
    except Exception as e:
        return 0


# 对网页内容进行正则匹配并处理
def addressList(content):
    #wiki:an identifier of 26-35 alphanumeric characters
    List = re.compile(r'\b1[a-km-z1-9A-HJ-NP-Z]{25,34}\b|\b3[a-km-z1-9A-HJ-NP-Z]{25,34}\b').findall(content)  # \b1[a-z0-9A-Z]{25,34}\b|\b3[a-z0-9A-Z]{25,34}\b   \b1\w{25,33}\b|\b3\w{25,33}\b
    # 去重
    List = list(set(List))
    return List

'''def xlsfile(file_name):
    writebook = xlwt.Workbook(encoding='utf-8')
    sheet = writebook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'序号', u'网址', u'描述', u'比特币地址', u'下载', u'备注']

    sheet.col(0).width = 256 * 5  # Set the column width
    sheet.col(1).width = 256 * 50  # Set the column width
    sheet.col(2).width = 256 * 20  # Set the column width
    sheet.col(3).width = 256 * 50  # Set the column width
    sheet.col(4).width = 256 * 5  # Set the column width
    sheet.col(5).width = 256 * 5  # Set the column width
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])

    writebook.save(file_name)
    return sheet
'''
#正确的搜索结果
def search_href(hrefs):
    new_list=[]
    for href in hrefs:
        #多余的谷歌相关链接
        if 'webcache.googleusercontent.com' not in href and 'google.com' not in href and '/search?cr=' not in href and 'http' in href:
            #某个不知名的浏览器加了前缀
            #href=str(href).replace('/url?q=','')
            #某个不知名的让链接带有sa，usg等参数的未知浏览器。。。
            #href=re.compile(r'http.*?(?=&sa=)').findall(href)
            new_list.append(href)
    return new_list

def googleSearch(wd, start, file_name):
    #print(headers)
    writebook = xlwt.Workbook(encoding='utf-8')
    sheet = writebook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'number', u'link', u'description', u'address', u'note']

    sheet.col(0).width = 256 * 5  # Set the column width
    sheet.col(1).width = 256 * 50  # Set the column width
    sheet.col(2).width = 256 * 20  # Set the column width
    sheet.col(3).width = 256 * 50  # Set the column width
    #sheet.col(4).width = 256 * 5  # Set the column width
    sheet.col(5).width = 256 * 5  # Set the column width
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    writebook.save(file_name)
    surl = "https://www.google.com/search"
    next_flag = 1
    url_flag=1
    pn=0
    row=1
    #禁用安全警告
    warnings.filterwarnings("ignore")
    #requests.packages.urllib3.disable_warnings()
    querystring = {'q': wd, 'filter': '0','cr':'countryUS','start':pn,'hl':'en','safe':'active'}
    #一直以next为下一次链接
    while next_flag:
        try:
            if url_flag:
                response = requests.get(surl, headers=headers, params=querystring, verify=False)
                selector = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))
                url_flag=0
            else:
                response = requests.get(surl,headers=headers,params=querystring, verify=False)
                selector = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))
            print('page:%d--------------------------------'%start)

            '''
            #with open ('page%d.txt'%start,'a',encoding='utf-8') as fp:
                fp.write(response.text)
                fp.close()
            '''
            s = requests.session()
            s.keep_alive = False
            #print(response.content)
            #此处修改下一页，除去tbody
            surl=selector.xpath('//*[@id="nav"]/tr/td[12]/a/@href')#//*[@id="pnnext"]/a/@href
            print('surl:'+str(surl))

            if len(surl)<1:
                next_flag=0
                print(response.content)
            else:
                surl = 'https://www.google.com' + str(surl[0])
            #获取hrefs，有待改进，再下一次层，见百度
            hrefs=selector.xpath('//*[@id="res"]//a/@href')
            #//*[@id="rso"]/div[1]/div/div[1]/div/div/div[1]/a
            #hrefs=re.compile(r'(?<=a href=\")http.*?(?=\")').findall(str(hrefs_context))
            hrefs=search_href(hrefs)
            #每页搜索条目数
            counts=len(hrefs)
            print(counts)
            count_h=0
            print('******************')
            while count_h<counts:
                s = requests.session()
                s.keep_alive = False
                time.sleep(5)
                try:
                    href=str(hrefs[count_h])
                    context_h = requests.get(href, timeout=20)  #
                    address_List=addressList(context_h.content.decode('utf-8'))
                    print("进入条目搜索："+href)
                    sheet.write(row, 0, str(row))
                    sheet.write(row, 1, href)
                    description = re.compile(r'(?<=://)\w*[\.\w*]+(?=\/)').findall(href)
                    sheet.write(row, 2, description)
                    num = len(address_List)
                    if num == 0:
                        sheet.write(row, 4, "Null")
                    if num == 1:
                        sheet.write(row, 3, address_List)
                    if num > 1:
                        sheet.write(row, 4, 'Multi')
                        address_str = ""
                        for address in address_List:
                            if verify(address)==1:
                                address_str += address
                                address_str += "\n"
                        sheet.write(row, 3, address_str)
                    #写一条保存
                    writebook.save(file_name)
                    row+=1
                except Exception as e:
                    print(e)
                    time.sleep(3)
                    #输出异常之后直接执行+1，无需continue
                    #continue
                count_h+=1
                # 写一页保存
                #writebook.save(file_name)
            start+=1
            pn = (start - 1) * 10
            querystring = {'start': pn}#修改pn值进入下一页（测试以下空是否可以）
            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(3)
            continue
# 主函数
if __name__ == '__main__':

    #关键词
    wd = "donate bitcoin"
    #起始页
    start = 1
    file_name = wd + ".xls"
    print("******************start********************")
    googleSearch(wd, start, file_name)
    print ("******************end********************")
