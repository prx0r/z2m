from ecom_agents.core import set_policy
from ecom_agents.models import MerchantPolicy
set_policy(MerchantPolicy(merchant_id='demo',currency='USD',max_auto_refund=50,max_auto_store_credit=150,max_auto_replacement_cost=75,allow_outbound_marketing_calls=False))
print('Seeded in-memory demo policy for this process.')
