'''
Created on 1 Apr 2021

@author: jacklok
'''

from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.customer_models import Customer
import trexmodel.conf as model_conf
from trexlib.utils.string_util import random_number, is_not_empty
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet,\
    MerchantUser
import logging
from trexlib.utils.common.cache_util import cache
from trexmodel import conf
from datetime import datetime

logger = logging.getLogger('model')


def generate_transaction_id(prefix=''):
    now                 = datetime.now()
    datetime_str        = now.strftime('%y%m%d%H%M%S')
    random_str_value    = random_number(6)
    
    return prefix[0:7] + datetime_str + random_str_value

class CustomerTransaction(BaseNModel, DictModel):
    '''
    
    '''
    transact_merchant       = ndb.KeyProperty(name="transact_merchant", kind=MerchantAcct)
    transact_outlet         = ndb.KeyProperty(name="transact_outlet", kind=Outlet)
    
    transact_datetime       = ndb.DateTimeProperty(required=True)
    created_datetime        = ndb.DateTimeProperty(required=True, auto_now=True)
    
    transaction_id          = ndb.StringProperty(required=True)
    invoice_id              = ndb.StringProperty(required=False)
    remarks                 = ndb.StringProperty(required=False)
    
    tax_amount              = ndb.FloatProperty(required=False, default=.0)
    transact_amount         = ndb.FloatProperty(required=True)
    
    
    transact_by             = ndb.KeyProperty(name="created_by", kind=MerchantUser)
    transact_by_username    = ndb.StringProperty(required=False)
    
    
    dict_properties         = ['transaction_id', 'invoice_id', 'remarks', 'tax_amount', 'transact_amount', 
                               'transact_datetime', 'created_datetime',  'transact_outlet_key', 'transact_outlet_details',
                               'transact_by_username']
    
    def to_transaction_details_json(self):
        pass
    
    @property
    def transact_customer_acct(self):
        return Customer.fetch(self.key.parent().urlsafe())
    
    @property
    def transact_merchant_acct(self):
        return MerchantAcct.fetch(self.transact_customer.urlsafe())
    
    @property
    def transact_outlet_key(self):
        return self.transact_outlet.urlsafe()
    
    @property
    def transact_outlet_details(self):
        return Outlet.fetch(self.transact_outlet.urlsafe())
    
    
    @staticmethod
    def create(customer, transact_amount=.0, tax_amount=.0, invoice_id=None, remarks=None, transact_outlet=None, transact_by=None, transact_datetime=None):
        
        if is_not_empty(transact_by):
            if isinstance(transact_by, MerchantUser):
                transact_by_username = transact_by.username

        
        transaction_id = generate_transaction_id()
        
        logger.debug('generated transaction_id=%s', transaction_id)
        logger.debug('invoice_id=%s', invoice_id)
        logger.debug('tax_amount=%s', tax_amount)
        logger.debug('transact_amount=%s', transact_amount)
        logger.debug('transact_by_username=%s', transact_by_username)
        
        customer_transaction = CustomerTransaction(
                                                    parent                  = customer.create_ndb_key(),
                                                    
                                                    transact_merchant       = customer.registered_merchant_acct.create_ndb_key(),
                                                    transact_outlet         = transact_outlet.create_ndb_key(),
                                                    
                                                    tax_amount              = tax_amount,
                                                    transact_amount         = transact_amount,
                                                    
                                                    transaction_id          = transaction_id,
                                                    invoice_id              = invoice_id,
                                                    remarks                 = remarks,
                                                    
                                                    transact_by             = transact_by.create_ndb_key(),
                                                    transact_by_username    = transact_by_username,
                                                    
                                                    transact_datetime       = transact_datetime,
                                                    )
        
        customer_transaction.put()
        
        return customer_transaction
    
    @staticmethod
    def list_customer_transaction(customer_acct, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key())
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def count_customer_transaction(customer_acct, limit=conf.MAX_FETCH_RECORD):
        query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key())
        
        return CustomerTransaction.count_with_condition_query(query, limit=limit)
        