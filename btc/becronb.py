# encoding: utf-8
import datetime
import random
import logging
import os
import sys
import time
import threading
from threading import Timer
import pymysql
from bs4 import BeautifulSoup
import requests
class Updatetable(object):
    pagesdic = {
        'btc': 'https://coinmarketcap.com/currencies/bitcoin/#markets',
        'eth': 'https://coinmarketcap.com/currencies/ethereum/#markets',
        'ltc': 'https://coinmarketcap.com/currencies/litecoin/#markets',
        'bch': 'https://coinmarketcap.com/currencies/bitcoin-cash/#markets',
        'zec': 'https://coinmarketcap.com/currencies/zcash/#markets',
        'eos': 'https://coinmarketcap.com/currencies/eos/#markets'
    }
    tables_dic = {
        'btc': [],
        'eth': [],
        'ltc': [],
        'bch': [],
        'zec': [],
        'eos': []
    }
    def __init__(self, coin='zec'):
        self.coin = coin
        self.firsttime =True

    def update_tables_dic(self):
        url = self.pagesdic[self.coin]
        print(url)
        html = requests.get(url)
        soup = BeautifulSoup(html.text,"lxml")
        table = soup.find('table', id="markets-table")

        row = 0

        for tr in table.tbody.find_all('tr'):  # 遍历每一个tr
            # print("key row=", key,row)
            # 将每一个tr的数据根据td查询出来，返回结果为list对象
            table_td_list = tr.find_all("td")
            td_text_list = []

            # print('table_td_list[0]:',table_td_list[0].find_element_by_css_selector('span.ng-binding.ng-scope').text)
            for td in table_td_list:  # 遍历每一个td
                td_text_list.append(td.text)  # 取出表格的数据，并放入行列表里

            if self.firsttime == True:
                # print('firsttime == True:',key)
                self.tables_dic[self.coin].append(td_text_list)
                # print(td_text_list)
            else:
                self.tables_dic[self.coin][row] = td_text_list
            row = row + 1
        self.firsttime = False

    def updatedb(self):
        print('updatedb:', self.coin)
        try:
            con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Lg152921', db='dbblkchain',
                                  charset='utf8')
            cur = con.cursor()
        except Exception as e:
            print('connect mysql e:',str(e))

        for r in self.tables_dic[self.coin]:
            cleanr_dic = self.washr(r)
            if cleanr_dic:
                cleanr_dic['m_coin']=self.coin
                cleanr_dic['m_symbol']=cleanr_dic['m_coin']+cleanr_dic['m_name']
                try:
                    #sql_str = "INSERT INTO btc_coins(m_symbol,m_name,m_coin,m_updatetime,m_price,m_24hvol,m_pair) values('{m_symbol}','{m_name}','{m_coin}','{m_updatetime}',{m_price},{m_24hvol},'{m_pair}') ON DUPLICATE KEY UPDATE m_updatetime='{m_updatetime}',m_price={m_price},m_pair='{m_pair}',m_24hvol={m_24hvol};".format(**cleanr_dic)
                    sql_str = "INSERT INTO btc_coins(m_symbol,m_name,m_coin,m_updatetime,m_price,m_24hvol,m_pair) values('{m_symbol}','{m_name}','{m_coin}','{m_updatetime}',{m_price},{m_24hvol},'{m_pair}') ON DUPLICATE KEY UPDATE m_updatetime='{m_updatetime}',m_price={m_price},m_pair='{m_pair}',m_24hvol={m_24hvol};".format(
                        **cleanr_dic)
                    print(sql_str)
                    cur.execute(sql_str)
                    con.commit()
                except Exception as e:
                    print(str(e))
        con.close()
#----utility--------
    def washr(self,row=[]):
        clean = {}
        # ['400', '\n\nLBank\n', 'ABT/BTC', '\n***\n\n$6,070,190\n\n', '\n***\n\n$5699.17\n\n', '\n0.00%\n', 'Spot', 'Percentage', 'Recently']
        if len(row) < 8:
            return clean
        try:
            clean['m_name'] = row[1].strip('\n')
            clean['m_updatetime'] = row[8]
            s=row[4].strip('\n')
            s1=s.split('$')
            clean['m_price'] = float(s1[1].replace(',', ''))

            s = row[3].strip('\n')
            s1 = s.split('$')
            clean['m_24hvol'] = float(s1[1].replace(',', ''))

            clean['m_pair'] = row[2]
        except Exception as e:
            print(str(e))

        return clean

    def updateweb(self):
        url = self.pagesdic[self.coin]
        print(url)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "lxml")
        table = soup.find('table', id="markets-table")

        row = 0

        for tr in table.tbody.find_all('tr'):  # 遍历每一个tr
            # print("key row=", key,row)
            # 将每一个tr的数据根据td查询出来，返回结果为list对象
            table_td_list = tr.find_all("td")
            table_a_list = tr.find_all("a")
            td_text_list = []

            # print('table_td_list[0]:',table_td_list[0].find_element_by_css_selector('span.ng-binding.ng-scope').text)
            #for td in table_td_list:  # 遍历每一个td
            #    td_text_list.append(td.text)  # 取出表格的数据，并放入行列表里

            for a in table_a_list:
                td_text_list.append(a)
            if self.firsttime == True:
                # print('firsttime == True:',key)
                self.tables_dic[self.coin].append(td_text_list)
                # print(td_text_list)
            else:
                self.tables_dic[self.coin][row] = td_text_list
            row = row + 1
        self.firsttime = False

        try:
            con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Lg152921', db='dbblkchain',
                                  charset='utf8')
            cur = con.cursor()
        except Exception as e:
            print('connect mysql e:',str(e))

        for web in self.tables_dic[self.coin]:
            cleanr_dic = {}
            try:
                if 'http' in str(web[0]):
                    t = str(web[1])
                    print('t0:',t)
                    l = t.split('>')
                    l1 = l[1].split('<')
                    cleanr_dic['m_name'] = l1[0]

                    t = str(web[0])
                    print('t1:', t)
                    l = t.split('"')
                    l1 = l[1].split('/')
                    cleanr_dic['m_website'] = l1[0] + '//' + l1[2] + '/'

                else:
                    t = str(web[0])
                    print('t0:',t)
                    l = t.split('>')
                    l1 = l[1].split('<')
                    cleanr_dic['m_name'] = l1[0]

                    t = str(web[1])
                    print('t1:',t   )
                    l = t.split('"')
                    l1 = l[1].split('/')
                    cleanr_dic['m_website'] = l1[0] + '//' + l1[2] + '/'
            except Exception as e:
                print(str(e))

            cleanr_dic['m_coin'] = self.coin
            cleanr_dic['m_symbol'] = cleanr_dic['m_coin'] + cleanr_dic['m_name']
            try:
                sql_str = "UPDATE btc_coins SET m_website = '{m_website}' WHERE m_symbol = '{m_symbol}'".format(
                    **cleanr_dic)
                cur.execute(sql_str)
                con.commit()
            except Exception as e:
                print(str(e))
        con.close()







