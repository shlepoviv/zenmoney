from enum import Enum

class AccauntType(Enum):
    cash = 'cash' 
    ccard = 'ccard' 
    checking = 'checking' 
    loan = 'loan' 
    deposit = 'deposit' 
    emoney = 'emoney' 
    debt = 'debt'


class EndDateOffsetInterval(Enum):
    day = 'day' 
    week = 'week' 
    month = 'month' 
    year = 'year'

class ReminderInterval(Enum):
    day = 'day' 
    week = 'week' 
    month = 'month' 
    year = 'year'

class PayoffInterval(Enum):
    month = 'month'
    year = 'year'

class ReminderState(Enum):
    planned = 'planned' 
    processed = 'processed' 
    deleted = 'deleted'