from apis.profiles import *
from apis.accounts import *
from apis.bills import *
from apis.search_bills import *
from apis.stats import *

# register API
api = endpoints.api_server([ProfilesApi, AccountsApi, BillsApi, SearchBillsApi, StatsApi])
