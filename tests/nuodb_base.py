#!/usr/bin/env python

import pynuodb
import pynuodb.entity
import tempfile
import unittest
import time

HOST            = "localhost"
DOMAIN_USER     = "domain"
DOMAIN_PASSWORD = "bird"

DBA_USER        = 'dba'
DBA_PASSWORD    = 'dba_password'
DATABASE_NAME   = 'pynuodb_test'

class NuoBase(unittest.TestCase):
    driver = pynuodb
    connect_args = ()
    options = {"schema": "test"}
    connect_kw_args = {'database': DATABASE_NAME, 'host': HOST, 'user': DBA_USER, 'password': DBA_PASSWORD, 'options': options }

    lower_func = 'lower' # For stored procedure test

    @classmethod
    def setUpClass(cls):
        domain = pynuodb.entity.Domain(HOST, DOMAIN_USER, DOMAIN_PASSWORD)
        try:
            if DATABASE_NAME not in [db.getName() for db in domain.getDatabases()]:
                peer = domain.getEntryPeer();
                peer.startStorageManager(DATABASE_NAME, tempfile.mkdtemp(), True, waitSeconds=10)
                peer.startTransactionEngine(DATABASE_NAME,  [('--dba-user', DBA_USER),('--dba-password', DBA_PASSWORD)], waitSeconds=10)
                
        finally:
            domain.disconnect()
            

    @classmethod
    def tearDownClass(cls):
        listener = TestDomainListener()
        domain = pynuodb.entity.Domain(HOST, DOMAIN_USER, DOMAIN_PASSWORD, listener)
        try:
            try:
                domain.getDatabase(DATABASE_NAME).shutdown(False)
            except:
                pass
            
            for i in xrange(1,20):
                time.sleep(0.25)
                if listener.db_left:
                    break
                
        finally:
            domain.disconnect()
            
            
    def _connect(self):
        return pynuodb.connect(**NuoBase.connect_kw_args)

class TestDomainListener(object):
    def __init__(self):
        self.db_left = False
            
    def databaseLeft(self, database):
        self.db_left = True

#
#if __name__ == '__main__':
#    unittest.main()
#    

