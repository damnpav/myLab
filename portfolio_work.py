from sqlalchemy import create_engine
import pyodbc


def connect_to_db():
    mysql_pass = open('/home/jet/Документы/mysql_pass.txt').readline()[:-1]
    try:
        engine = create_engine('mysql+pymysql://root:'+mysql_pass+'@localhost:3306/portfolios')
        conn = engine.connect()
    except Exception as e:
        return 'Error: ' + str(e)
    return conn, engine


def close_connection(credentials):
    credentials[0].close()  # connection
    credentials[1].dispose()  # engine


def open_position(conn, stock, buy_date, buy_price, volume, comment):
    query = f'INSERT INTO vtb (Stock, BuyDate, BuyPrice, Volume, Comments) ' \
            f'VALUES (\'{stock}\', \'{buy_date}\', {buy_price}, {volume}, \'{comment}\') '
    conn.execute(query)


# TODO: session
def close_position(conn, paper_id, sell_date, sell_price):
    query = f'INSERT INTO portfolios.vtb_history \n ' \
            f'(PaperId, Stock, BuyDate, BuyPrice, Volume, Comments, SellDate, SellPrice) \n ' \
            f'SELECT PaperId, Stock, BuyDate, BuyPrice, Volume, Comments, \'{sell_date}\', {sell_price} \n ' \
            f'from portfolios.vtb WHERE PaperId = {paper_id}; \n '
    conn.execute(query)
    query = f'DELETE FROM portfolios.vtb WHERE PaperId = {paper_id};'
    conn.execute(query)





