# -*- coding: utf-8 -*-

import MySQLdb
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine

from settings import DATABASE

def get_engine():
    if (DATABASE.get('SSH')):
        SSH = DATABASE['SSH']
        server = SSHTunnelForwarder(
            (SSH['HOST'], SSH['PORT']),
            ssh_username=SSH['USER'],
            ssh_password=SSH['PASS'],
            remote_bind_address=(DATABASE['HOST'], DATABASE['PORT'])
        )
        server.start()
        return create_engine(
            f"mysql+mysqldb://{DATABASE['USER']}:{DATABASE['PASS']}@127.0.0.1:{server.local_bind_port}/{DATABASE['DB']}?charset=utf8"
            , echo=True
        )
    
    return create_engine(
        f"mysql+mysqldb://{DATABASE['USER']}:{DATABASE['PASS']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB']}?charset=utf8"
        , echo=True
    )

def test(engine):
    select = 'select * from BSM_TJ100KAMOKU_VERSION_KANRI_MASTER'
    print(list(engine.execute(select)))

if __name__ == "__main__":
    engine = get_engine()
    test(engine)
