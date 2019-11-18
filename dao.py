import json
import const
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="twitter_pool",
                                                              pool_size=const.POOL_SIZE,
                                                              pool_reset_session=True,
                                                              host=const.HOST,
                                                              database=const.DATABASE,
                                                              user=const.USERNAME,
                                                              password=const.PASSWORD)


# get api key and secret to connect to bnb client.
def getAllUsername():
    conn = connection_pool.get_connection()
    cur = conn.cursor()
    try:
        sql = '''select username_id from info'''
        cur.execute(sql)
        data = cur.fetchall()
        return data
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()
    return None

def checkExists(username_id):
    conn = connection_pool.get_connection()
    cur = conn.cursor()
    try:
        sql = '''select count(*) from info where username_id = %s''' %username_id
        cur.execute(sql)
        data = cur.fetchone()
        return data[0]
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()
    return None

def getSymbol(username_id):
    conn = connection_pool.get_connection()
    cur = conn.cursor()
    try:
        sql = '''select symbol from info where username_id = %s''' %username_id
        cur.execute(sql)
        data = cur.fetchone()
        return data[0]
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()
    return None

def insertTwitter(username, username_id):
    conn = connection_pool.get_connection()
    cur = conn.cursor()
    try:
        sql = "INSERT INTO info(username,username_id) VALUES('{}',{})".format(
            username,
            username_id)
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print("insertError  error " + str(e))
    finally:
        cur.close()
        conn.close()

def getKeyword():
    conn = connection_pool.get_connection()
    cur = conn.cursor()
    try:
        sql = '''select keyword from keyword where status = 1'''
        cur.execute(sql)
        data = cur.fetchall()
        return data
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()
    return None