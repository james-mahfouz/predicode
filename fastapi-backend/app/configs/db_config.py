import time
from mongoengine import connect, get_db
from configs.config import DB_NAME, DB_HOST, DB_PORT


def db_connection_keep_on():
    connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)
    db = get_db()

    if db.name != 'predicode_db':
        print('db connection sleeping for 5 seconds')
        time.sleep(5)
        print('Trying to reconnect')
        db_connection_keep_on(client=client)
    else:
        print('DB connected Successfully')
        return db
