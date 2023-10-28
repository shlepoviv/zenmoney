from typing import Optional

from datetime import datetime, date

from pydantic import BaseModel, Field
from pydantic.types import UUID, List, Decimal

from src.enums import AccauntType, ReminderInterval, ReminderState

class ServerTimestamp(BaseModel):
    servertimestamp:    datetime


class Instrument(BaseModel):
    id :        int
    changed:    datetime
    title:      str
    shortTitle: str
    symbol:     str
    rate:       Decimal

class Country(BaseModel):
    id:        int
    title:     str
    currency:  int
    domain:    Optional[str]

class Company(BaseModel):
    id:        int
    changed:   datetime
    title:     str
    fullTitle: Optional[str]
    www:       Optional[str]
    country:   Optional[int]

class ZenmoneyUser(BaseModel):
    id:       int
    changed:  datetime
    login:    Optional[str]
    currency: int  # Instrument.id
    parent:   Optional[int]


class Account(BaseModel):
    id:         UUID
    changed:    datetime
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id
    role:       Optional[int] # zenmoneyuser.id
    instrument: Optional[int] # Instrument.id
    company:    Optional[int] # Company.id
    type:       AccauntType
    title:      str
    syncID:     Optional[List[str]]

    balance:      Decimal
    startBalance: Decimal
    creditLimit:  Decimal = Field(ge = 0)

    inBalance:        bool
    savings:          Optional[bool]
    enableCorrection: bool
    enableSMS:        bool
    archive:          bool

	#//Для счетов с типом отличных от 'loan' и 'deposit' в  этих полях можно ставить null
    # capitalization: Optional[bool]
    # percent: Optional[Decimal]
    # startDate: Optional[datetime]
    # endDateOffset: Optional[int]
    # endDateOffsetinterval: Optional[EndDateOffsetInterval]
    # payoffStep: Optional[int]
    # payoffinterval: Optional[PayoffInterval]


class Tag(BaseModel):
    id:      UUID
    changed: datetime 
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id

    title:   str
    parent:  Optional[str] # Tag.id
    icon:    Optional[str]
    picture: Optional[str]
    color:   Optional[int]

    showIncome:    bool
    showOutcome:   bool
    budgetIncome:  bool
    budgetOutcome: bool	
    required:      Optional[bool]

class Merchant(BaseModel):
    id:      UUID
    changed: datetime
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id
    title:   str

class Reminder(BaseModel):
    id:      UUID
    changed: datetime
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id

    incomeInstrument:  int    # Instrument.id
    incomeAccount:     str # Account.id
    income:            Decimal = Field(ge=0)
    outcomeInstrument: int    # Instrument.id
    outcomeAccount:    str # Account.id
    outcome:           Decimal = Field(ge=0)

    tag:      Optional[List[str]]  # Tag.id
    merchant:  Optional[str] # Merchant.id
    payee:     Optional[str]
    comment:   Optional[str]

    interval: Optional[ReminderInterval]
    step:    Optional[int] = Field(ge=0)
    points: Optional[int] = Field(ge=0)
    startDate: datetime
    endDate:   Optional[datetime]
    notify: bool

class ReminderMarker(BaseModel):
    id:      UUID
    changed: datetime
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id

    incomeInstrument:  int    # Instrument.id
    incomeAccount:     str # Account.id
    income:            Decimal = Field(ge=0)
    outcomeInstrument: int    # Instrument.id
    outcomeAccount:    str # Account.id
    outcome:           Decimal = Field(ge=0)

    tag:       Optional[List[str]]  # Tag.id
    merchant:  Optional[str] # Merchant.id
    payee:     Optional[str]
    comment:   Optional[str]

    date: datetime

    reminder: str # Reminder.id
    state: ReminderState

    notify: bool


class Transaction(BaseModel):
    id:      UUID
    changed: datetime
    created: datetime
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id
    deleted: bool
    hold:    Optional[bool]

    incomeInstrument:  int    # Instrument.id
    incomeAccount:     str # Account.id
    income:            Decimal = Field(ge=0)
    outcomeInstrument: int    # Instrument.id
    outcomeAccount:    str # Account.id
    outcome:           Decimal = Field(ge=0)

    tag:      Optional[List[str]]  # Tag.id
    merchant:  Optional[str] # Merchant.id
    payee:         Optional[str]
    originalPayee: Optional[str]
    comment:       Optional[str]

    date: date

    mcc: Optional[int] = Field(default=None)

    reminderMarker: Optional[str] # ReminderMarker.id

    opIncome:            Optional[Decimal] 
    opIncomeInstrument:  Optional[int] # Instrument.id
    opOutcome:           Optional[Decimal]
    opOutcomeInstrument: Optional[int] # Instrument.id

    latitude:  Optional[Decimal]
    longitude: Optional[Decimal]

class Budget(BaseModel):
    changed: datetime 
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id

    tag:  Optional[str] # Tag.id | '00000000-0000-0000-0000-000000000000'
    date: datetime

    income:      Decimal
    incomeLock:  bool
    outcome:     Decimal
    outcomeLock: bool

class Deletion(BaseModel):
    id:     str  # String -> Object.id
    object: str # String -> Object.class
    stamp:  int
    zenmoneyuser:    int= Field(alias='user')  # zenmoneyuser.id


class Diff(BaseModel):

    serverTimestamp:        datetime = Field(default=None)

    forceFetch: List[str] = Field(default=None)# [String -> Object.class]?

    instrument:     List[Instrument] = Field(default=None)
    company:        List[Company] = Field(default=None)
    zenmoneyuser:   List[ZenmoneyUser] = Field(default=None,alias='user') 
    account:        List[Account] = Field(default=None)
    tag:            List[Tag] = Field(default=None)
    merchant:       List[Merchant] = Field(default=None)
    budget:         List[Budget] = Field(default=None)
    reminder:       List[Reminder] = Field(default=None)
    reminderMarker: List[ReminderMarker] = Field(default=None)
    transaction:    List[Transaction] = Field(default=None)
    country:        List[Country] = Field(default=None)

    deletion:       List[Deletion] = Field(default=None)


if __name__ == '__main__':
    d = Diff.model_construct()