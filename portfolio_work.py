from sqlalchemy import create_engine


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


def close_position(conn, paper_id, sell_date, sell_price):
    query = f'USE portfolios; \n ' \
            f'START TRANSACTION; \n ' \
            f'INSERT INTO vtb_history \n (Stock, BuyDate, BuyPrice, Volume, Comments, SellDate, SellPrice) \n ' \
            f'SELECT Stock, BuyDate, BuyPrice, Volume, Comments, \'{sell_date}\', {sell_price} \n ' \
            f'from vtb WHERE PaperId = {paper_id}; \n ' \
            f'DELETE FROM vtb WHERE PaperId = {paper_id}; \n ' \
            f'COMMIT; '
    print(query)
    conn.execute(query)







