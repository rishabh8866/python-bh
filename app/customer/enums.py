import enum

class CurrencyEnum(enum.Enum):
    INR = "inr"
    USD = "usd"
    EUR = "euro"

class TimeDisplayEnum(enum.Enum):
    M1 = "12 hr"
    M2 = "24 hr"

class TypeEnum(enum.Enum):
    FREE = "free"
    PAID = "paid"

class NumberDisplayEnum(enum.Enum):
    M1 = "m1"
    M2 = "m2"

class PropertyEnum(enum.Enum):
    NORMAL = 'normal'
    RENTED = "rented"

class DateDisplayEnum(enum.Enum):
    M1 = "dd/mm/yyyy"
    M2 = "mm/dd/yyyy"
