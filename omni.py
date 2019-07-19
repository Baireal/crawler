# -*-coding:utf-8 -*-
import requests,json,time
import xlwt

def omni(start):
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
    }
    book_name = "D:/Program Files/PyCharm 2018.3.3/PycharmProject/one/USDT/omni/%d_%d.xls" % (start,start-step+1)
    writebook = xlwt.Workbook(encoding='utf-8')
    sheet = writebook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'区块号', u'数目', u'币种', u'时间', u'发送地址', u'接收地址', u'交易']
    sheet.col(0).width = 256 * 8
    sheet.col(1).width = 256 * 15
    sheet.col(2).width = 256 * 10
    sheet.col(3).width = 256 * 20
    sheet.col(4).width = 256 * 40
    sheet.col(5).width = 256 * 40
    sheet.col(6).width = 256 * 8
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    row = 1
    writebook.save(book_name)

    for i in range(start,start-step,-1):
        #print ('page %d'%i)
        surl = 'https://api.omniexplorer.info/v1/transaction/block/%d' % i
        try:
            response = requests.request("GET", surl, headers=headers,timeout=30)
            wbdata=response.text
            s = requests.session()
            s.keep_alive = False
            data = json.loads(wbdata)
            trans = data['transactions']
            for tran in trans:
                try:
                    block= tran['block']
                    sheet.write(row, 0, block)
                    blocktime = tran['blocktime']
                    t = time.localtime(blocktime)
                    blocktime = time.strftime("%Y/%m/%d %H:%M:%S", t)
                    sheet.write(row, 3, blocktime)
                    valid = tran['valid']
                    sheet.write(row, 6, valid)
                    sendingaddress = tran['sendingaddress']
                    sheet.write(row, 4, sendingaddress)
                    referenceaddress = tran['referenceaddress']
                    sheet.write(row, 5, referenceaddress)


                    amount = tran['amount']
                    sheet.write(row, 1, amount)
                    propertyname = tran['propertyname']
                    sheet.write(row, 2, propertyname)
                    row += 1
                except Exception as e:
                    print (e)
                    row += 1
                    continue

            writebook.save(book_name)
        except Exception as e:
            print(e,"page %d"%i)
            with open('D:/Program Files/PyCharm 2018.3.3/PycharmProject/one/USDT/omni/omni_wrong.txt','a')as fp:
                fp.write(str(i))
                fp.write('\n')
            continue
        #页面最多10/s访问
        time.sleep(0.5)

# 主函数
if __name__ == '__main__':
    #开始区块
    start = 571491
    #结束区块
    end = 567962
    #每个文件步长
    step = 20
    print("**************** start *********************")
    for i in range(start,end,-step):
        print('start:%d end:%d'%(i,i-step))
        omni(i)
    print("****************  end  *********************")

