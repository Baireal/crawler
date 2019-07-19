# -*-coding:utf-8 -*-
import urllib2,xlwt,requests,random,linecache

from lxml import etree
#爬取ins>=100，outs>=10的地址信息
def transSearch():
    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36",#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    }

    '''n = random.randrange(1, 37)  # 1-9中生成随机数
    # 从文件poem.txt中对读取第a行的数据
    proxy = linecache.getline('1.txt', n)
    
    proxy = proxy.replace('\n', '')
    proxy = '27.208.141.126:8060'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }'''

    book_name = "exchange_in_out.xls"
    writebook = xlwt.Workbook(encoding='utf-8')
    sheet = writebook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'序号', u'交易所', u'比特币地址',u'转入',u'转出',u'排名']

    sheet.col(0).width = 256 * 5  # Set the column width
    sheet.col(1).width = 256 * 20  # Set the column width
    sheet.col(2).width = 256 * 50  # Set the column width
    sheet.col(3).width = 256 * 8  # Set the column width
    sheet.col(4).width = 256 * 8  # Set the column width
    sheet.col(5).width = 256 * 5  # Set the column width

    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    writebook.save(book_name)
    row = 1
    for page in range(1,101):
        while 1:#出现异常继续进入该页面
            try:
                print ("page %d--------"%page)
                surl ='https://bitinfocharts.com/top-100-richest-bitcoin-addresses-%d'%page+'.html'# 'https://www.blockchain.com/zh-cn/btc/tags?filter=8'
                context = requests.request("GET", surl, headers=headers)
                selector = etree.HTML(context.text, parser=etree.HTMLParser(encoding='utf-8'))
                #print context.text
                s = requests.session()
                s.keep_alive = False
                '''
                top1_list=selector.xpath(u'//table[@id="tblOne"]/tbody/tr/td[1]/text()')
                print top1_list
                #address1_list = selector.xpath(u'//table[@id="tblOne"]/tbody/tr/td[2]/a/text()')
                #address1_list = selector.xpath(u'//table[@id="tblOne"]/tbody/tr/td[2]/small/parent::td/a/text()')
                # address1_list = selector.xpath(u'//table[@id="tb10ne"]/tbody/tr/td[2]/small/../a/text()')

                top2_list = selector.xpath(u'//table[@id="tblOne2"]/tbody/tr/td[1]/text()')
                #wallet2_list = selector.xpath(u'//table[@id="tblOne2"]/tbody/tr/td[2]/small/a/text()')
                #address2_list = selector.xpath(u'//table[@id="tblOne2"]/tbody/tr/td[2]/a/text()')
                for top1 in top1_list:
                    print top1
                    top1=str(top1)
                    in1=selector.xpath('//td[text()='+str(top1)+']/following-sibling::td[6]/text()')
                    print in1
                    print "..."
                    out1=selector.xpath('//td[text()='+str(top1)+')]/following-sibling::td[9]/text()')
                    print out1
                    wallet1 = selector.xpath('//td[text()='+str(top1)+')]/following-sibling::td[1]/small/a/text()')
                    print wallet1
                    address1=selector.xpath('//td[text()='+str(top1)+')]/following-sibling::td[1]/a/text()@href')
                    print address1
                '''
                top1_list=selector.xpath(u'//table[@id="tblOne"]/tbody/tr')
                for top1 in top1_list:
                    rank1=top1.xpath('.//td[1]/text()')
                    in1 = top1.xpath('.//td[7]/text()')
                    out1 = top1.xpath('.//td[10]/text()')
                    wallet1 = top1.xpath('.//td[2]/small/a/text()')
                    address1 = top1.xpath('.//td[2]/a/text()')
                    if len(in1)>0 and len(out1)>0:
                        if int(in1[0]) >= 100 and int(out1[0]) >= 10:
                            sheet.write(row, 3, in1[0])
                            sheet.write(row, 4, out1[0])
                            sheet.write(row, 0, str(row))
                            if len(wallet1) == 0:
                                sheet.write(row, 1, '')
                            else:
                                sheet.write(row, 1, wallet1[0])
                            sheet.write(row, 2, address1[0])
                            sheet.write(row, 5, rank1[0])
                            row += 1
                writebook.save(book_name)


                '''
                for top2 in top2_list:
                    in2=selector.xpath('//td[text()='+str(top2)+')]/following-sibling::td[6]/text()')
                    out2=selector.xpath('//td[text()='+str(top2)+')]/following-sibling::td[9]/text()')
                    wallet2 = selector.xpath('//td[text()='+str(top2)+')]/following-sibling::td[1]/small/a/text()')
                    address2 = selector.xpath('//td[text()='+str(top2)+')]/following-sibling::td[1]/a/text()@href')
                '''
                #这里省去tbody！！！
                top2_list = selector.xpath(u'//table[@id="tblOne2"]/tr')
                for top2 in top2_list:
                    rank2 = top2.xpath('.//td[1]/text()')
                    in2 = top2.xpath('.//td[7]/text()')
                    out2 = top2.xpath('.//td[10]/text()')
                    wallet2 = top2.xpath('.//td[2]/small/a/text()')
                    address2 = top2.xpath('.//td[2]/a/text()')
                    if len(in2) > 0 and len(out2) > 0:
                        if int(in2[0]) >= 100 and int(out2[0]) >= 10:
                            sheet.write(row, 3, in2[0])
                            sheet.write(row, 4, out2[0])
                            sheet.write(row, 0, str(row))
                            if len(wallet2) == 0:
                                sheet.write(row, 1, '')
                            else:
                                sheet.write(row, 1, wallet2[0])
                            sheet.write(row, 2, address2[0])
                            sheet.write(row, 5, rank2[0])
                            row += 1
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


