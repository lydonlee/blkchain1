# encoding: utf-8
import datetime
import random
import logging
import os
import sys
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchWindowException
import time
import threading
from threading import Timer
import pymysql
from selenium.webdriver.support.select import Select

pagesdic ={
                'btc':'https://www.cryptocompare.com/coins/btc/markets/USD',
                'eth':'https://www.cryptocompare.com/coins/eth/markets/USD',
                'ltc':'https://www.cryptocompare.com/coins/ltc/markets/USD',
                'bch':'https://www.cryptocompare.com/coins/bch/markets/USD',
                'zec':'https://www.cryptocompare.com/coins/zec/markets/USD',
                'eos':'https://www.cryptocompare.com/coins/eos/markets/USD'

}
tables_dic = {
                'btc':[],
                'eth':[],
                'ltc':[],
                'bch':[],
                'zec':[],
                'eos':[]
              }
website_dic={
'Bitstamp':'https://www.bitstamp.net/',
'Bitwage':'https://bitwage.com/',
'Coinmama':'https://coinmama.com/',
'Kraken':'https://www.kraken.com/',
'Bisq':'https://bisq.network/',
'Hodl Hodl':'https://hodlhodl.com/',
'Local Bitcoins':'https://localbitcoins.com/',
'Paxful':'https://paxful.com/',
'Indodax':'https://indodax.com/',
'Bit2C':'https://www.bit2c.co.il/',
'Bits of Gold':'https://www.bitsofgold.co.il/',
'BtcBox':'https://www.btcbox.co.jp/',
'Luno':'https://www.luno.com/',
'Luno':'https://www.luno.com/',
'Bithumb':'https://www.bithumb.com/',
'Coinone':'https://coinone.co.kr/',
'Korbit':'https://www.korbit.co.kr/',
'Koinim':'https://www.koinim.com/',
'BitOasis':'https://bitoasis.net/',
'Karsha':'https://karsha.biz/',
'AnyCoin Direct':'https://anycoindirect.eu/',
'Bitcoin.de':'https://www.bitcoin.de/',
'BitPanda':'https://www.bitpanda.com/',
'BL3P':'https://bl3p.eu/',
'Paymium':'https://www.paymium.com/',
'The Rock Trading':'https://therocktrading.com/',
'BitBay':'https://www.bitbay.net/',
'Kuna':'https://kuna.io/',
'Bittylicious':'https://bittylicious.com/',
'CoinCorner':'https://www.coincorner.com/',
'Coinfloor':'https://www.coinfloor.co.uk/',
'Luno':'https://www.luno.com/',
'iceCUBED':'https://www.ice3x.com/',
'Luno':'https://www.luno.com/',
'Canadian Bitcoins':'https://www.canadianbitcoins.com/',
'Quadriga CX':'https://www.quadrigacx.com/',
'QuickBT':'https://quickbt.com/',
'BitMae':'https://www.bitmae.com/',
'Bitso':'https://bitso.com/',
'Volabit':'https://www.volabit.com/',
'Gemini':'https://gemini.com/',
'itBit':'https://www.itbit.com/',
'ArgenBTC':'https://argenbtc.com/',
'Bitex':'https://bitex.la/',
'Buenbit':'https://www.buenbit.com/',
'SatoshiTango':'https://www.satoshitango.com/',
'3xbit':'https://3xbit.com.br/',
'Foxbit':'https://foxbit.com.br/',
'Mercado Bitcoin':'https://www.mercadobitcoin.com.br/',
'OmniTrade':'https://www.omnitrade.io/',
'Walltime':'https://walltime.info/',
'Buda':'https://www.buda.com/',
'Buda':'https://www.buda.com/',
'Buda':'https://www.buda.com/',
'Cryptobuyer':'https://www.cryptobuyer.io/',
'Bitcoin Australia':'https://bitcoin.com.au/',
'CoinJar':'https://www.coinjar.com/',
'CoinLoft':'https://www.coinloft.com.au/',
'CoinSpot':'https://www.coinspot.com.au/',
'CoinTree':'https://www.cointree.com.au/',
'HardBlock':'https://www.hardblock.net/',
'Independent Reserve':'https://www.independentreserve.com/',
'Independent Reserve':'https://www.independentreserve.com/',
'Kiwi-coin':'https://kiwi-coin.com/',
'OKCoin':'http://www.okex.com'
}
rundriver = False

def startget_table_content():
    global rundriver
    if rundriver == True:
        print("driver is runing,please use 'stopedriver()' to stop it first")
        return
    rundriver = True
    for k, values in tables_dic.items():
        t = threading.Thread(target=update_tables_dic, args=(k,values))
        t.start()
        time.sleep(30)
    time.sleep(10)

    t = threading.Thread(target=updatetables_dic)
    t.start()
    print("end startget_table_content")

def updatetables_dic():
    global rundriver
    i = 0
    try:
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Lg152921', db='dbblkchain',
                              charset='utf8')
        cur = con.cursor()
    except Exception as e:
        print('connect mysql e:',str(e))

    while rundriver:
        for k, table in tables_dic.items():
            for r in table:
                cleanr_dic = washr(r)
                if cleanr_dic:
                    cleanr_dic['m_coin']=k
                    cleanr_dic['m_symbol']=cleanr_dic['m_coin']+cleanr_dic['m_name']
                    try:
                        sql_str = "replace into btc_coinbar(m_symbol,m_name,m_coin,m_updatetime,m_price,m_24hvol,m_24hprice,m_24hchange,m_24hchangepercent) values('{m_symbol}','{m_name}','{m_coin}','{m_updatetime}',{m_price},{m_24hvol},{m_24hprice},'{m_24hchange}','{m_24hchangepercent}')".format(**cleanr_dic)
                        cur.execute(sql_str)
                        con.commit()
                    except Exception as e:
                        print(str(e))


        i = i+1
        print("while true i",i)
        time.sleep(60)
    print("kill updatetables_dic!")
    con.close()

def washr(row = [] ):
        clean = {}
    #['Bitfinex\n3 min ago', '$ 132.41', '$ 126.88', 'L: $ 124.66\nH: $ 133.20', 'ZEC 0.4847\n$ 64.18', 'ZEC 10,818.38\n$ 1,383,491.86', '$ 5.53 4.36%']
        if len(row) < 7:
            return clean
        try:
            li = row[0].split('\n')
            clean['m_name']= li[0]
            clean['m_updatetime']=li[1]
            clean['m_price'] = float(row[1].strip('$').replace(',',''))

            li = row[5].split('\n')
            clean['m_24hvol'] = float(li[1].strip('$').replace(',',''))
            clean['m_24hprice'] = float(li[0][3:].replace(',',''))

            li = row[6].split()
            clean['m_24hchange'] = li[1]
            clean['m_24hchangepercent'] = li[2]

        except Exception as e:
            print(str(e))
            print("m_24hchange li:", li)

        return clean

#  File "/Users/liligong/blkchainsite/btc/bedriver.py", line 86, in washr
#    clean['m_price'] = float(row[1].strip('$'))
#ValueError: could not convert string to float: ' 6,426.78'

def update_tables_dic(key = 'zec',table_list=[]):
    global rundriver
    print(key,table_list)
    sum = 0
    firsttime  = True

    browser = geturl(pagesdic[key])

    t = Timer(1800, browser.refresh)
    t.start
    while rundriver:
        try:
        # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
            table_tr_list = browser.find_element_by_css_selector('table.table.table-striped.table-streamer.text-right').find_elements(By.TAG_NAME, "tr")
            row = 0

            for tr in table_tr_list:  # 遍历每一个tr
                #print("key row=", key,row)
            # 将每一个tr的数据根据td查询出来，返回结果为list对象
                table_td_list = tr.find_elements(By.TAG_NAME, "td")
                td_text_list = []

                #print('table_td_list[0]:',table_td_list[0].find_element_by_css_selector('span.ng-binding.ng-scope').text)
                for td in table_td_list:  # 遍历每一个td
                    td_text_list.append(td.text)  # 取出表格的数据，并放入行列表里

                if firsttime == True:
                    #print('firsttime == True:',key)
                    table_list.append(td_text_list)
                    #print(td_text_list)
                else:
                    #print('else td_text_list:',key,td_text_list)
                    if len(td_text_list):  # 有时候取出来的值是空，如果时空就不更新
                        if len(td_text_list[0]):
                            table_list[row] = td_text_list

                row = row + 1
            #print(table_list)
            firsttime = False
            time.sleep(30)
        except Exception as e:
            print('exction e:',str(e))
            print("excption from find_elements sum=",sum,key)
            sum = sum+1
            if sum == 5:
                browser.refresh()
    print("kill update_tables_dic,coin:",key)
def stopdriver():
    global rundriver
    rundriver = False

def getlastupdate():
    try:
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Lg152921', db='dbblkchain',
                              charset='utf8')
        cur = con.cursor()
    except Exception as e:
        print('connect mysql e:',str(e))
    sql_str = "select ifnull(update_time, create_time) from information_schema.`TABLES` where table_schema = database() and table_name = 'btc_coinbar'"
    cur.execute(sql_str)
    # 获取所有记录列表
    results = cur.fetchall()
    con.close()
    return results[0][0]

def geturl(url = ''):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2,
                 'profile.default_content_setting_values' :{'notifications' : 2}
        }
        chrome_options.add_experimental_option("prefs", prefs)

        #browser = webdriver.Chrome('/Users/liligong/anaconda/lib/python3.6/site-packages/chromedriver',
        #                           chrome_options=chrome_options)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.implicitly_wait(10)
        try:
            browser.get(url)
        except TimeoutException:
            print("TimeoutException")

        return browser


def updatewebsite():
        #broswer = geturl('https://bitcoin.org/en/exchanges')
        #web_list = broswer.find_elements_by_class_name("no_toc anchorAf")
        #for web in web_list:
        #    print("'"+web.text+"'"+':'+"'"+web.get_attribute('href')+"'"+',')
        for k in website_dic:
            sql = "UPDATE btc_coinbar SET m_website='{0}' WHERE m_name = '{1}';".format(website_dic[k],k)
            print(sql)
            results_list = execsql(sql)


def execsql(sql_str=''):
    try:
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Lg152921', db='dbblkchain')
        cur = con.cursor()
    except Exception as e:
        print('connect mysql e:',str(e))
    cur.execute(sql_str)
    con.commit()
    # 获取所有记录列表
    results = cur.fetchall()
    con.close()
    return results
"""
con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Lg152921', db='dbblkchain',charset='utf8')
cur = con.cursor()
li = ['Bitfinex\n3 min ago', '$ 132.41', '$ 126.88', 'L: $ 124.66\nH: $ 133.20', 'ZEC 0.4847\n$ 64.18', 'ZEC 10,818.38\n$ 1,383,491.86', '$ 5.53 4.36%']
cleanr_dic=be.washr(li)
cleanr_dic['m_coin']='ZEC'
cleanr_dic['m_symbol']=cleanr_dic['m_coin']+cleanr_dic['m_name']
sql_str = "replace into btc_coinbar(m_symbol,m_name,m_coin,m_updatetime,m_price,m_24hvol,m_24hprice,m_24hchange,m_24hchangepercent) values('{m_symbol}','{m_name}','{m_coin}','{m_updatetime}',{m_price},{m_24hvol},{m_24hprice},{m_24hchange},'{m_24hchangepercent}')".format(**cleanr_dic)
cur.execute(sql_str)
con.commit()

listcoinprice=[]
listexchanges=[
    ['sitename','www','BTC' ,'ETH' ,'BCH' ,'LTC' ,'EOS','0' ],
    ['okex',"https://www.okcoin.com/",'div#quotation ul.quotation-imgs li:nth-child(1) div:nth-child(2) span','div#quotation ul.quotation-imgs li:nth-child(3) div:nth-child(2) span','div#quotation ul.quotation-imgs li:nth-child(5) div:nth-child(2) span','div#quotation ul.quotation-imgs li:nth-child(2) div:nth-child(2) span','','1'],
    ['bitstamp',"https://www.bitstamp.net/",'table#live-state-trades-mobile tbody tr td:nth-child(2)','table#live-state-trades-mobile tbody tr td:nth-child(2)','table#live-state-trades-mobile tbody tr td:nth-child(2)','table#live-state-trades-mobile tbody tr td:nth-child(2)','','2'],
    ['huobipro','https://www.hbg.com/en-us/','div.coin_list dl dd div span:nth-child(3)','div.coin_list dl:nth-child(4) dd div span:nth-child(3)','div.coin_list dl:nth-child(3) dd div span:nth-child(3)','div.coin_list dl:nth-child(6) dd div span:nth-child(3)','div.coin_list dl:nth-child(7) dd div span:nth-child(3)','3'],
    ['58coin','https://www.58coin.com/','div.market.flex-box.flex-direction-row.flex-justify-between.flex-align-item-start.flex-wrap-nowrap div:nth-child(1) p:nth-child(2)','div.market.flex-box.flex-direction-row.flex-justify-between.flex-align-item-start.flex-wrap-nowrap div:nth-child(3) p:nth-child(2)','div.market.flex-box.flex-direction-row.flex-justify-between.flex-align-item-start.flex-wrap-nowrap div:nth-child(4) p:nth-child(2)','div.market.flex-box.flex-direction-row.flex-justify-between.flex-align-item-start.flex-wrap-nowrap div:nth-child(5) p:nth-child(2)','div.market.flex-box.flex-direction-row.flex-justify-between.flex-align-item-start.flex-wrap-nowrap div:nth-child(2) p:nth-child(2)','4'],
    ['asbtc','https://www.asbtc.com/','tbody.tab_body tr:nth-child(2) td:nth-child(2)','tbody.tab_body tr:nth-child(4) td:nth-child(2)','tbody.tab_body tr:nth-child(6) td:nth-child(2)','tbody.tab_body tr:nth-child(5) td:nth-child(2)','tbody.tab_body tr:nth-child(3) td:nth-child(2)','5']

]
def startgetprice():
    t = threading.Thread(target=printlistprice)
    t.start()
    for i in range(1,6):
        t = threading.Thread(target=getprice, args=(i,))
        t.start()

def getprice(i=1):
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome('/Users/liligong/anaconda/lib/python3.6/site-packages/chromedriver',chrome_options=chrome_options)
    browser.implicitly_wait(10)

    try:
        browser.get(listexchanges[i][1])
        time.sleep(30)
        while True:
            for j in range(2, 7):
                try:
                    preparepage(browser, listexchanges[i][0], j)
                    coinprice = browser.find_element_by_css_selector(listexchanges[i][j])
                    print(listexchanges[0][j], coinprice.text)
                    cleanprice = washdata(listexchanges[i][0], coinprice.text)
                    listcoinprice[i][j] = cleanprice

                except NoSuchWindowException:
                    print("NoSuchWindowException:", listexchanges[0][j])
                except NoSuchElementException:
                    print("NoSuchElementException:", listexchanges[0][j])



    except TimeoutException:
        print("TimeoutException")
        getprice(url, priceid)

def test(i=1):
    print("URL=",listexchanges[i][1])

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome('/Users/liligong/anaconda/lib/python3.6/site-packages/chromedriver',chrome_options=chrome_options)
    browser.implicitly_wait(10)
    try:
        browser.get(listexchanges[i][1])
        time.sleep(10)
    except TimeoutException:
        print("TimeoutException")
        test(i)

            #btcprice = WebDriverWait(browser, 60).until(EC.presence_of_element_located(By.cssSelector(priceid)))
    for j in range(2,7):
        try:
            preparepage(browser,listexchanges[i][0],j)
            coinprice = browser.find_element_by_css_selector(listexchanges[i][j])
            print(listexchanges[0][j], coinprice.text)
            cleanprice = washdata(listexchanges[i][0],coinprice.text)
            listcoinprice[i][j]=cleanprice
            print('cleanprice',listcoinprice[i][j])

        except NoSuchWindowException:
            print("NoSuchWindowException:",listexchanges[0][j])
        except NoSuchElementException:
            print("NoSuchElementException:",listexchanges[0][j])

def washdata(exchange='okex',coinprice='5000'):
    if exchange == listexchanges[5][0]:
        #asbtc 返回的数据
        #BTC 7372.31/￥50057.984
        #ETH 6.488/￥44.053
        listhead = coinprice.split('/')
        return listhead[0][4:]
    elif exchange == listexchanges[3][0]:
        #huobipro返回数据
        #561.55 ≈$561.55
        listhead = coinprice.split('≈')
        return listhead[0]
    return coinprice

def preparepage(driver ,exchange = 'bitstamp',j=2):
    if exchange == listexchanges[2][0]:#bitstamp 需要点击页面选择对应币种
        try:
            sel = driver.find_element_by_id('overview-pairs-mobile')
            if j == 2:
                Select(sel).select_by_value("BTC/USD")
            elif j==3:
                #如果是ETH ,点击对应选择
                Select(sel).select_by_value("ETH/USD")
            elif j == 4:
                #如果是BCH
                Select(sel).select_by_value("BCH/USD")
            elif j == 5:
                #LTC
                Select(sel).select_by_value("LTC/USD")
            elif j == 6:
                #EOS,bitstap没有eos
                pass

            time.sleep(5)
        except:
           print("preparepage exception:", sys.exc_info()[0])

    else:
        pass


def testdic():
    mydic = {
        'btc': [],
        'eth': []
    }
    sec_dic ={}
    btc_list = [['bitstamp','35000'],['okex','3400']]
    ltc_list = [['bitstamp', '200'], ['okex', '180']]

    mydic['btc'] = btc_list
    mydic['ltc'] = ltc_list
    for k, values in mydic.items():
        for i in values:
            sec_dic['k'] = k
            print(k)
            print(sec_dic)

def testlist():
    mylist = [
        ['58coin', 'www.58', 'key58'],
        ['ok', 'www.okcoin', 'ok'],
        ['bitstap', 'www.bits', 'keybits']
    ]
    otlist = ['szdsk','wefsf','wfwfwfi','ew2r322']
    slist = [23,2323]

    mylist[0] = otlist
    mylist[1] = slist

    print(mylist)

def printlistprice():
        while True:
            print("listcoinprice:",listcoinprice)
            time.sleep(20)

def testmysql():
    con = pymysql.connect(host='127.0.0.1',port = 3306,user ='root',password='Lg152921',db='dbblkchain',charset = 'utf8')
    cur = con.cursor()
    cur.execute("replace into btc_coinbar(m_symbol,m_name,m_coin,m_price) values('btcBitfinex','Bitfinex','btc',54321)")
    con.commit()
    cur.execute("select*from btc_coinbar")
now = datetime.datetime.now()
tim_str = 'UPDATE btc_Modelupdatetime SET m_coinbar= '01 01 2018 13:12AM'{new_time}'.format(new_time = now)
"""
"""
select ifnull(update_time , create_time) from information_schema.`TABLES` where table_schema=database() and table_name='btc_coinbar';
http://www.zb.com（原中比特）
http://www.huobi.pro（火币国际站）
http://www.okex.com（OK国际站）
http://www.aex.com（原比特时代）
cex.com（原币久网）
gate.io（原比特儿）
http://www.bite.ceo（CEO交易所）
http://www.coinw.com(币赢网)
binance.com(币安网)

https://www.bestbitcoinexchange.io/visit/EN/broker/etoro
 https://www.bestbitcoinexchange.io/visit/EN/broker/24option
 https://www.bestbitcoinexchange.io/visit/EN/broker/coinbull
 https://www.bestbitcoinexchange.io/visit/EN/broker/luno
 https://www.bestbitcoinexchange.io/visit/EN/broker/paxforex
 https://www.bestbitcoinexchange.io/visit/EN/broker/binance
 https://www.bestbitcoinexchange.io/visit/EN/broker/coinbase
 https://www.bestbitcoinexchange.io/visit/EN/broker/localbitcoins
 https://www.bestbitcoinexchange.io/visit/EN/broker/cex
 https://www.bestbitcoinexchange.io/visit/EN/broker/changelly
 https://www.bestbitcoinexchange.io/visit/EN/broker/coinmama
 https://www.bestbitcoinexchange.io/visit/EN/broker/xtrade
 https://www.bestbitcoinexchange.io/visit/EN/broker/capital
 https://www.bestbitcoinexchange.io/visit/EN/broker/paxful
 https://www.bestbitcoinexchange.io/visit/EN/broker/kraken
 https://www.bestbitcoinexchange.io/visit/EN/broker/poloniex
 https://www.bestbitcoinexchange.io/visit/EN/broker/gemini
 https://www.bestbitcoinexchange.io/visit/EN/broker/bithumb
 https://www.bestbitcoinexchange.io/visit/EN/broker/xcoins
 https://www.bestbitcoinexchange.io/visit/EN/broker/cobinhood
 https://www.bestbitcoinexchange.io/visit/EN/broker/coincheck
 https://www.bestbitcoinexchange.io/visit/EN/broker/coinexchange
 https://www.bestbitcoinexchange.io/visit/EN/broker/shapeshift
 https://www.bestbitcoinexchange.io/visit/EN/broker/bitso
 https://www.bestbitcoinexchange.io/visit/EN/broker/indacoin
 https://www.bestbitcoinexchange.io/visit/EN/broker/city-index
 https://www.bestbitcoinexchange.io/visit/EN/broker/bitbay
 https://www.bestbitcoinexchange.io/visit/EN/broker/bitstamp
 https://www.bestbitcoinexchange.io/visit/EN/broker/cryptopia
 https://www.bestbitcoinexchange.io/visit/EN/broker/gdax
 https://www.bestbitcoinexchange.io/visit/EN/broker/kucoin
 https://www.bestbitcoinexchange.io/visit/EN/broker/bitpanda
 https://www.bestbitcoinexchange.io/visit/EN/broker/foxbit
 https://www.bestbitcoinexchange.io/visit/EN/broker/bitflyer
 https://www.bestbitcoinexchange.io/visit/EN/broker/bitfinex
 https://www.bestbitcoinexchange.io/visit/EN/broker/bit-z
 https://www.bestbitcoinexchange.io/visit/EN/broker/quadriga
 https://www.bestbitcoinexchange.io/visit/EN/broker/bigone
 https://www.bestbitcoinexchange.io/visit/EN/broker/lakebtc
 https://www.bestbitcoinexchange.io/visit/EN/broker/wex
 https://www.bestbitcoinexchange.io/visit/EN/broker/kuna
 https://www.bestbitcoinexchange.io/visit/EN/broker/yobit
 https://www.bestbitcoinexchange.io/visit/EN/broker/zebpay
 https://www.bestbitcoinexchange.io/visit/EN/broker/hitbtc
 https://www.bestbitcoinexchange.io/visit/EN/broker/bx-in-th
 
 国际
Bitstamp https://www.bitstamp.net/
Bitwage https://bitwage.com/
Coinmama https://coinmama.com/
Kraken https://www.kraken.com/

点对点
Bisq https://bisq.network/
Hodl Hodl https://hodlhodl.com/
Local Bitcoins https://localbitcoins.com/
Paxful https://paxful.com/

印尼
Indodax https://indodax.com/

以色列
Bit2C https://www.bit2c.co.il/
Bits of Gold https://www.bitsofgold.co.il/
BtcBox https://www.btcbox.co.jp/
Luno https://www.luno.com/
Luno https://www.luno.com/
Bithumb https://www.bithumb.com/
Coinone https://coinone.co.kr/
Korbit https://www.korbit.co.kr/
Koinim https://www.koinim.com/
BitOasis https://bitoasis.net/
Karsha https://karsha.biz/
AnyCoin Direct https://anycoindirect.eu/
Bitcoin.de https://www.bitcoin.de/
BitPanda https://www.bitpanda.com/
BL3P https://bl3p.eu/
Paymium https://www.paymium.com/
The Rock Trading https://therocktrading.com/
BitBay https://www.bitbay.net/
Kuna https://kuna.io/
Bittylicious https://bittylicious.com/
CoinCorner https://www.coincorner.com/
Coinfloor https://www.coinfloor.co.uk/
Luno https://www.luno.com/
iceCUBED https://www.ice3x.com/
Luno https://www.luno.com/
Canadian Bitcoins https://www.canadianbitcoins.com/
Quadriga CX https://www.quadrigacx.com/
QuickBT https://quickbt.com/
BitMae https://www.bitmae.com/
Bitso https://bitso.com/
Volabit https://www.volabit.com/
Gemini https://gemini.com/
itBit https://www.itbit.com/
ArgenBTC https://argenbtc.com/
Bitex https://bitex.la/
Buenbit https://www.buenbit.com/
SatoshiTango https://www.satoshitango.com/
3xbit https://3xbit.com.br/
Foxbit https://foxbit.com.br/
Mercado Bitcoin https://www.mercadobitcoin.com.br/
OmniTrade https://www.omnitrade.io/
Walltime https://walltime.info/
Buda https://www.buda.com/
Buda https://www.buda.com/
Buda https://www.buda.com/
Cryptobuyer https://www.cryptobuyer.io/
Bitcoin Australia https://bitcoin.com.au/
CoinJar https://www.coinjar.com/
CoinLoft https://www.coinloft.com.au/
CoinSpot https://www.coinspot.com.au/
CoinTree https://www.cointree.com.au/
HardBlock https://www.hardblock.net/
Independent Reserve https://www.independentreserve.com/
Independent Reserve https://www.independentreserve.com/
Kiwi-coin https://kiwi-coin.com/

con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='mysql')
junyunshidai

/root/anaconda3/bin:
export PATH="$PATH:/home/liligong/anaconda3/bin"
export PATH=/Users/liligong/Documents/programe/apache-maven-3.3.3/bin:$PATH
# Setting PATH for Python 3.6
# The original version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin:${PATH}"
export PATH

# added by Anaconda3 4.4.0 installer
export PATH="/home/liligong/anaconda3/bin:$PATH"
export PATH="/home/liligong/anaconda3/lib/python3.6/site-packages:$PATH"
export PATH="/Users/liligong/Documents/programe/mysql-5.6.27-osx10.9-x86_64/bin:$PATH"

echo 'export PATH="/home/liligong/anaconda3/lib/python3.6/site-packages:$PATH"' >> ~/.bashrc
sudo mv chromedriver /home/liligong/anaconda3/bin/chromedriver
sudo chmod u+x,o+x   /home/liligong/anaconda3/bin/chromedriver
"""
