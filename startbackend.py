from btc.becronb import Updatetable
def updateweb():
    for key, values in Updatetable.pagesdic.items():
        coin =Updatetable(key)
        coin.updateweb()

def startbe():
    for key,values in Updatetable.pagesdic.items():
        print(key)
        coin = Updatetable(key)
        coin.update_tables_dic()
        coin.updatedb()

if __name__ == '__main__':
    startbe()
    #updateweb()

