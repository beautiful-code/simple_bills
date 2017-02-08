from api_imports import *

@endpoints.api(name='stats',
                version='v1',
                allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID],
                scopes=[EMAIL_SCOPE])
class StatsApi(remote.Service):
    @endpoints.method(AccountMessage, AccountStatsMessage,
            path='accountStatsOnDemand',
            http_method='POST', name='accountStatsOnDemand')
    def accountStatsOnDemand(self, request):
        user=endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId)
        account = Account.get(accountId)

        year_bill_counts = account.year_bill_counts()

        asm = AccountStatsMessage()
        asm.bill_count = sum(year_bill_counts.values())
        for year in year_bill_counts.keys():
            ysm = YearStatsMessage()
            ysm.year = year
            ysm.bill_count = year_bill_counts[year]

            # Get distinct months
            month_bill_counts = account.month_bill_counts(year)
            for month in month_bill_counts.keys():
                msm = MonthStatsMessage()
                msm.month = month
                msm.bill_count = month_bill_counts[month]
                ysm.month_stats.append(msm)

            asm.year_stats.append(ysm)

        return asm
