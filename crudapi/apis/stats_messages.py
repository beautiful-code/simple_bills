from protorpc import messages

class MonthStatsMessage(messages.Message):
    month = messages.IntegerField(1)
    bill_count = messages.IntegerField(2)


class YearStatsMessage(messages.Message):
    year = messages.IntegerField(1)
    bill_count = messages.IntegerField(2)
    month_stats = messages.MessageField(MonthStatsMessage, 3, repeated=True)

class AccountStatsMessage(messages.Message):
    bill_count = messages.IntegerField(1)
    year_stats = messages.MessageField(YearStatsMessage, 2, repeated=True)

