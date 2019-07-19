# -*-coding:utf-8 -*-
import requests,json,time,re
import xlwt
from lxml import etree


def ethusd(start):
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
    }
    #存储xls的位置
    book_name = "D:/Program Files/PyCharm 2018.3.3/PycharmProject/one/USDT/ethUSD/%d_%d.xls" % (start,start-step)
    writebook = xlwt.Workbook(encoding='utf-8')
    sheet = writebook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'区块号', u'数目', u'时间', u'发送地址', u'接收地址', u'交易']
    sheet.col(0).width = 256 * 8  # Set the column width
    sheet.col(1).width = 256 * 10  # Set the column width
    sheet.col(2).width = 256 * 25  # Set the column width
    sheet.col(3).width = 256 * 40  # Set the column width
    sheet.col(4).width = 256 * 40  # Set the column width
    sheet.col(5).width = 256 * 8  # Set the column width
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    row = 1
    writebook.save(book_name)
    for i in range(start,start-step,-1):
        while 1:
            print ('page %d'%i)
            surl = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&mode=&m=normal&p=%d'%i
            try:

                response = requests.request("GET", surl, headers=headers,timeout=20)
                selector = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
                s = requests.session()
                s.keep_alive = False
                usd_list = selector.xpath(u'//*[@id="maindiv"]/div[2]/table/tbody/tr')
                url_list = selector.xpath(u'//*[@id="maindiv"]/div[2]/table/tbody/tr/td[1]/span/a/@href')
                for usd, url in zip(usd_list, url_list):
                    time = usd.xpath('.//td[2]/span/@title')
                    sheet.write(row, 2, time[0])
                    try:
                        url_inside = 'https://etherscan.io' + str(url)
                        response = requests.request("GET", url_inside, headers=headers, timeout=20)
                        selector = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
                        s = requests.session()
                        s.keep_alive = False
                        '''
                        time = selector.xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[4]/div[2]/text()')
                        print(time[0])
                        t = re.compile(r'(?<=\().*M').findall(time[0])
                        sheet.write(row, 2, t)
                        print(t)
                        '''

                        send = selector.xpath('//*[@id="wrapperContent"]/li/div/span[2]/a/text()')
                        sheet.write(row, 3, send[0])
                        receive = selector.xpath('//*[@id="wrapperContent"]/li/div/span[4]/a/text()')
                        sheet.write(row, 4, receive[0])

                        num = selector.xpath('//*[@id="wrapperContent"]/li/div/span[6]/text()')
                        sheet.write(row, 1, num[0])

                        block=selector.xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[3]/div[2]/a/text()')
                        sheet.write(row, 0, block[0])
                        status = selector.xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[2]/div[2]/span/text()')
                        status = str(status[0]).replace('\"','')
                        sheet.write(row, 5, status)
                        row += 1
                    except Exception as e:
                        print(e)
                        with open('ethusd_url_wrong.txt', 'a')as fp:
                            fp.write(url)
                            fp.write('\n')
                        row += 1
                        continue

                writebook.save(book_name)
                break
            except Exception as e:
                print("page failed:" + str(e))
                continue


def etheur(page):
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
    }
    #存储xls的位置
    book_name = "D:/Program Files/PyCharm 2018.3.3/PycharmProject/one/USDT/ethEUR/1_4.xls"
    writebook = xlwt.Workbook(encoding='utf-8')
    sheet = writebook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'区块号', u'数目', u'时间', u'发送地址', u'接收地址', u'交易']
    sheet.col(0).width = 256 * 8  # Set the column width
    sheet.col(1).width = 256 * 10  # Set the column width
    sheet.col(2).width = 256 * 25  # Set the column width
    sheet.col(3).width = 256 * 40  # Set the column width
    sheet.col(4).width = 256 * 40  # Set the column width
    sheet.col(5).width = 256 * 8  # Set the column width
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    row = 1
    writebook.save(book_name)
    for i in range(1,page+1):
        while 1:
            print ('page %d'%i)
            surl = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0xabdf147870235fcfc34153828c769a70b3fae01f&mode=&m=normal&p=%d'%i
            try:

                response = requests.request("GET", surl, headers=headers,timeout=20)
                selector = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
                s = requests.session()
                s.keep_alive = False
                eur_list = selector.xpath(u'//*[@id="maindiv"]/div[2]/table/tbody/tr')
                url_list = selector.xpath(u'//*[@id="maindiv"]/div[2]/table/tbody/tr/td[1]/span/a/@href')
                for eur, url in zip(eur_list, url_list):
                    time = eur.xpath('.//td[2]/span/@title')
                    sheet.write(row, 2, time[0])
                    try:
                        url_inside = 'https://etherscan.io' + str(url)
                        response = requests.request("GET", url_inside, headers=headers, timeout=20)
                        selector = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
                        s = requests.session()
                        s.keep_alive = False

                        send = selector.xpath('//*[@id="wrapperContent"]/li/div/span[2]/a/text()')
                        sheet.write(row, 3, send[0])
                        receive = selector.xpath('//*[@id="wrapperContent"]/li/div/span[4]/a/text()')
                        sheet.write(row, 4, receive[0])

                        num = selector.xpath('//*[@id="wrapperContent"]/li/div/span[6]/text()')
                        sheet.write(row, 1, num[0])

                        block = selector.xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[3]/div[2]/a/text()')
                        sheet.write(row, 0, block[0])
                        status = selector.xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[2]/div[2]/span/text()')
                        status = str(status[0]).replace('\"', '')
                        sheet.write(row, 5, status)

                        row += 1
                    except Exception as e:
                        print(e)
                        with open('etheur_url_wrong.txt', 'a')as fp:
                            fp.write(url)
                            fp.write('\n')
                        row += 1
                        continue

                writebook.save(book_name)
                break
            except Exception as e:
                print("page failed:"+str(e))
                continue

# 主函数
if __name__ == '__main__':


    #选择币种 n :ethusd = 1  etheur = 2
    n = 1


    if n == 1:
        #开始页
        start = 1
        #步长
        step = 30
        #终止页
        end = 4000
        print("**************** start *********************")
        for i in range(end, start, -step):
            print('-----------------new xls------------------')
            ethusd(i)
        print("****************  end  *********************")
    else:
        print("**************** eur *********************")
        #目前的总页数
        page = 4
        etheur(page)