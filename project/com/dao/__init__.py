import pymysql

def con_db():

    return pymysql.connect(host='localhost', user='root', password='root', db='ccs', cursorclass=pymysql.cursors.DictCursor)