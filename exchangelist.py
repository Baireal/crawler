# -*-coding:utf-8 -*-
import urllib2,xlwt,requests

from lxml import etree
#只爬取有标记wallet的
def transSearch():
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'connection': "close",
    }

    book_name = "exchange.xls"
    writebook = xlwt.Workbook(encoding='utf-8')
    sheet = writebook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'序号', u'交易所', u'比特币地址',u'排名']

    sheet.col(0).width = 256 * 5  # Set the column width
    sheet.col(1).width = 256 * 20  # Set the column width
    sheet.col(2).width = 256 * 50  # Set the column width

    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    writebook.save(book_name)
    row = 1
    for page in range(1,101):

        while 1:
            try:
                print ("page %d--------"%page)
                surl ='https://bitinfocharts.com/top-100-richest-bitcoin-addresses-%d'%page+'.html'# 'https://www.blockchain.com/zh-cn/btc/tags?filter=8'
                context = requests.request("GET", surl, headers=headers)
                selector = etree.HTML(context.text, parser=etree.HTMLParser(encoding='utf-8'))

                '''test1 = selector.xpath('//table[@id="tblOne"]/tr')
                test2= selector.xpath('//table[@id="tblOne"]/tbody/tr')
                print test1
                print test2'''



                top1_list=selector.xpath(u'//table[@id="tblOne"]/tbody/tr/td[1]/text()')
                wallet1_list = selector.xpath(u'//table[@id="tblOne"]/tbody/tr/td[2]/small/a/text()')
                address1_list = selector.xpath(u'//table[@id="tblOne"]/tbody/tr/td[2]/small/parent::td/a/text()')
                # address1_list = selector.xpath(u'//table[@id="tb10ne"]/tbody/tr/td[2]/small/../a/text()')

                #这里注意tbody！！！
                top2_list = selector.xpath(u'//table[@id="tblOne2"]/tr/td[1]/text()')
                wallet2_list = selector.xpath(u'//table[@id="tblOne2"]/tr/td[2]/small/a/text()')
                address2_list = selector.xpath(u'//table[@id="tblOne2"]/tr/td[2]/small/parent::td/a/text()')

                count=0
                for wallet1 in wallet1_list:
                    sheet.write(row, 0, str(row))
                    sheet.write(row, 1, wallet1)
                    sheet.write(row, 2, address1_list[count])
                    sheet.write(row, 3, top1_list[count])
                    count+=1
                    row+=1
                #writebook.save(book_name)

                count=0
                for wallet2 in wallet2_list:
                    sheet.write(row, 0, str(row))
                    sheet.write(row, 1, wallet2)
                    sheet.write(row, 2, address2_list[count])
                    sheet.write(row, 3, top2_list[count])
                    count+=1
                    row+=1
                writebook.save(book_name)
                break
            except Exception as e:
                print(e)
                continue



# 主函数
if __name__ == '__main__':
    print ("start--------------")
    transSearch()
    print ("end----------------")


