'''
Created on 22 Apr 2021

@author: jacklok
'''
from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel, FullTextSearchable
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet, MerchantUser
from trexmodel.models.datastore.program_models import MerchantProgram
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.voucher_models import MerchantVoucher
from trexmodel.models.datastore.transaction_models import generate_transaction_id
import trexmodel.conf as model_conf
from trexlib.utils.string_util import is_not_empty, is_empty
import logging
from trexlib.utils.common.cache_util import cache
from trexlib.utils.common.date_util import convert_date_to_datetime
from trexmodel import conf, program_conf
from trexlib.utils.string_util import random_string
from six import string_types
from datetime import datetime


logger = logging.getLogger('model')


class RewardEntitlement(BaseNModel, DictModel):
    effective_date              = ndb.DateProperty(required=True)
    expiry_date                 = ndb.DateProperty(required=True)
    
    transaction_id              = ndb.StringProperty(required=True)
    invoice_id                  = ndb.StringProperty(required=False)
    
    sales_amount                = ndb.FloatProperty(required=True, default=.0)
    tax_amount                  = ndb.FloatProperty(required=True, default=.0)
    
    rewarded_datetime           = ndb.DateTimeProperty(required=True, auto_now_add=True)
    rewarded_by                 = ndb.KeyProperty(name="rewarded_by", kind=MerchantUser)
    rewarded_by_username        = ndb.StringProperty(required=False)
    
    reward_datetime_provided    = ndb.BooleanProperty(required=False, default=False)

class CustomerEntitledReward(RewardEntitlement):
    '''
    Customer as ancestor
    '''
    
    merchant_acct               = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct)
    user_acct                   = ndb.KeyProperty(name="user_acct", kind=User)
    transact_outlet             = ndb.KeyProperty(name="transact_outlet", kind=Outlet)
    reward_program              = ndb.KeyProperty(name="reward_program", kind=MerchantProgram)
    
    

class CustomerCountableReward(CustomerEntitledReward):
    reward_amount               = ndb.IntegerProperty(required=True, default=0)
    used_reward_amount          = ndb.IntegerProperty(required=True, default=0)
    
    @classmethod
    def create(cls, reward_amount, customer_acct, transact_outlet,
               effective_date=None, expiry_date=None, 
               transaction_id=None, invoice_id=None,
               rewarded_by=None):
        
        if is_empty(transaction_id):
            transaction_id = generate_transaction_id()
            
        if effective_date is None:
            effective_date = datetime.today()
        
        customer_reward = cls(
                                            parent                  = customer_acct.create_ndb_key(),
                                            reward_amount           = reward_amount,
                                            transaction_id          = transaction_id,
                                            invoice_id              = invoice_id,
                                            
                                            merchant_acct           = customer_acct.merchant_acct,
                                            transact_outlet         = transact_outlet.create_ndb_key(),
                                            
                                            effective_date          = effective_date,
                                            expiry_date             = expiry_date,
                                            
                                            rewarded_by             = rewarded_by.create_ndb_key(),
                                            rewarded_by_username    = rewarded_by.username,
                                            
                                            )
        
        customer_reward.put()
        
        return customer_reward
        
class CustomerPointReward(CustomerCountableReward):
    pass

class CustomerStampReward(CustomerCountableReward):
    pass
    
            
    
    
class CustomerEntitledVoucher(CustomerEntitledReward):
    
    entitled_voucher            = ndb.KeyProperty(name='entitled_voucher', kind=MerchantVoucher)
    
    redeem_code                 = ndb.StringProperty(required=False)
    redeemed_datetime           = ndb.DateTimeProperty(required=False)
    
    redeemed_by_outlet          = ndb.KeyProperty(name='redeemed_by_outlet', required=False)
    redeemed_by                 = ndb.KeyProperty(name="redeemed_by", kind=MerchantUser)
    redeemed_by_username        = ndb.StringProperty(required=False)
    
    redeemed_transaction_id     = ndb.StringProperty(required=False)
    
    is_redeemed                 = ndb.BooleanProperty(required=False, default=False)
    is_reverted                 = ndb.BooleanProperty(required=False, default=False)   
    
    removed_datetime            = ndb.DateTimeProperty(required=False)
    removed_by_username         = ndb.StringProperty(required=False)
    
    
    dict_properties     = ['redeem_code', 'voucher_configuration', 'rewarded_by_username', 'rewarded_datetime', 'transaction_id', 
                           'invoice_id', 'merchant_reference_code', 'tags_list', 
                           'registered_outlet_key', 'registered_merchant_acct_key', 'registered_datetime', 'modified_datetime']
    
    @property
    def transact_outlet_summary(self):
        return Outlet.fetch(self.transact_outlet.urlsafe())
    
    @property
    def voucher_configuration(self):
        voucher = MerchantVoucher.fetch(self.entitled_voucher.urlsafe())
        if voucher:
            return voucher.to_configuration()
    
    
    @staticmethod
    def create(entitled_voucher, customer_acct, transact_outlet, 
               transaction_id=None, invoice_id=None,
               rewarded_by=None):
        
        redeem_code = random_string(program_conf.REDEEM_CODE_LENGTH, is_human_mistake_safe=True)
        
        if is_empty(transaction_id):
            transaction_id = generate_transaction_id()
        
        customer_entiteld_voucher = CustomerEntitledVoucher(
                                            parent                  = customer_acct.create_ndb_key(),
                                            entitled_voucher        = entitled_voucher.create_ndb_key(),
                                            
                                            redeem_code             = redeem_code,
                                            transaction_id          = transaction_id,
                                            invoice_id              = invoice_id,
                                            
                                            merchant_acct           = customer_acct.merchant_acct,
                                            transact_outlet         = transact_outlet.create_ndb_key(),
                                            
                                            rewarded_by             = rewarded_by.create_ndb_key(),
                                            rewarded_by_username    = rewarded_by.username,
                                            
                                            )
        
        customer_entiteld_voucher.put()
        
        
    @staticmethod
    def get_by_redeem_code(redeem_code):
        return  CustomerEntitledVoucher.query(CustomerEntitledVoucher.redeem_code==redeem_code).get()
    
    
    