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

chrome_options = webdriver.ChromeOptions()
chrome_options.set_headless(headless=True)
""""
chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size={}x{}'.format(*self.window_size)

prefs = {"profile.managed_default_content_settings.images": 2,
         'profile.default_content_setting_values': {'notifications': 2}
         }
chrome_options.add_experimental_option("prefs", prefs)
"""
class Updatetable(object):
    pagesdic = {
        'btc': 'https://www.cryptocompare.com/coins/btc/markets/USD',
        'eth': 'https://www.cryptocompare.com/coins/eth/markets/USD',
        'ltc': 'https://www.cryptocompare.com/coins/ltc/markets/USD',
        'bch': 'https://www.cryptocompare.com/coins/bch/markets/USD',
        'zec': 'https://www.cryptocompare.com/coins/zec/markets/USD',
        'eos': 'https://www.cryptocompare.com/coins/eos/markets/USD'

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
        self.key = coin
        self.firsttime = True

    def init(self):
        try:
            print('initing:',self.key)
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
        except Exception as e:
            print('webdriver.Chrome exction e:', str(e))
            self.init()
            return
        self.geturl()
        try:
            WebDriverWait(self.browser, 120, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table.table-striped.table-streamer.text-right')))
        except Exception as e:
            print('WebDriverWait e:', str(e))
            return
            # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
        self.table_tr_list = self.browser.find_element_by_css_selector(
            'table.table.table-striped.table-streamer.text-right').find_elements(By.TAG_NAME, "tr")
        print('sucess initing:', self.key)

    def updatedb(self):
        print('updatedb:', self.key)
        try:
            con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Lg152921', db='dbblkchain',
                                  charset='utf8')
            cur = con.cursor()
        except Exception as e:
            print('connect mysql e:',str(e))

        for r in self.tables_dic[self.key]:
            cleanr_dic = self.washr(r)
            if cleanr_dic:
                cleanr_dic['m_coin']=self.key
                cleanr_dic['m_symbol']=cleanr_dic['m_coin']+cleanr_dic['m_name']
                try:
                    sql_str = "replace into btc_coinbar(m_symbol,m_name,m_coin,m_updatetime,m_price,m_24hvol,m_24hprice,m_24hchange,m_24hchangepercent) values('{m_symbol}','{m_name}','{m_coin}','{m_updatetime}',{m_price},{m_24hvol},{m_24hprice},'{m_24hchange}','{m_24hchangepercent}')".format(**cleanr_dic)
                    cur.execute(sql_str)
                    con.commit()
                except Exception as e:
                    print(str(e))
        con.close()

    def update_tables_dic(self):
        row = 0
        try:
            for tr in self.table_tr_list:  # 遍历每一个tr
                # print("key row=", key,row)
                # 将每一个tr的数据根据td查询出来，返回结果为list对象
                table_td_list = tr.find_elements(By.TAG_NAME, "td")
                td_text_list = []

                # print('table_td_list[0]:',table_td_list[0].find_element_by_css_selector('span.ng-binding.ng-scope').text)
                for td in table_td_list:  # 遍历每一个td
                    td_text_list.append(td.text)  # 取出表格的数据，并放入行列表里

                if self.firsttime == True:
                    # print('firsttime == True:',key)
                    self.tables_dic[self.key].append(td_text_list)
                    # print(td_text_list)
                else:
                    # print('else td_text_list:',key,td_text_list)
                    if len(td_text_list):  # 有时候取出来的值是空，如果时空就不更新
                        if len(td_text_list[0]):
                            self.tables_dic[self.key][row] = td_text_list
                        else:
                            print(self.key,"get empty td_text_list[0]! refesh!")
                    else:
                        print(self.key,"get empty td_text_list!")
                row = row + 1
            self.firsttime = False
        except Exception as e:
            print('update_tables_dic Exception:',str(e))
            self.update_tables_dic()

#----utility--------
    def washr(self,row=[]):
        clean = {}
        # ['Bitfinex\n3 min ago', '$ 132.41', '$ 126.88', 'L: $ 124.66\nH: $ 133.20', 'ZEC 0.4847\n$ 64.18', 'ZEC 10,818.38\n$ 1,383,491.86', '$ 5.53 4.36%']
        if len(row) < 7:
            return clean
        try:
            li = row[0].split('\n')
            clean['m_name'] = li[0]
            clean['m_updatetime'] = li[1]
            clean['m_price'] = float(row[1].strip('$').replace(',', ''))

            li = row[5].split('\n')
            clean['m_24hvol'] = float(li[1].strip('$').replace(',', ''))
            clean['m_24hprice'] = float(li[0][3:].replace(',', ''))

            li = row[6].split()
            clean['m_24hchange'] = li[1]
            clean['m_24hchangepercent'] = li[2]

        except Exception as e:
            print(str(e))

        return clean

    def geturl(self):
        try:
            self.browser.get(self.pagesdic[self.key])
            print('title',self.browser.title)
        except Exception as e:
            print('exction e:', str(e))
            self.geturl()

    def refresh(self):
        self.browser.refresh()

        WebDriverWait(self.browser, 120, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table.table-striped.table-streamer.text-right')))
        # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
        self.table_tr_list = self.browser.find_element_by_css_selector(
            'table.table.table-striped.table-streamer.text-right').find_elements(By.TAG_NAME, "tr")

    def quit(self):
        self.browser.quit()

