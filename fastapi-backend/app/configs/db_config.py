import time

def db_connection_keep_on(client):
    db = client

    if db.name != 'predicode_db':
        print('db connection sleeping for 5 seconds')
        time.sleep(5)
        print('Trying to reconnect')
        db_connection_keep_on(client=client)
    else:
        print('DB connected Successfully')
        return db
