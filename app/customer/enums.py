import enum

class CurrencyEnum(enum.Enum):
    CAD = "CAD"
    USD = "USD"
    EUR = "EUR"
    CHF = "CHF"
    GDP = "GDP"
    

class TimeDisplayEnum(str,enum.Enum):
    AM_PM = "AM/PM"
    H = "24 H"

class TypeEnum(enum.Enum):
    FREE = "free"
    PAID = "paid"

class NumberDisplayEnum(str,enum.Enum):
    M1 = "1,000.00"
    M2 = "1'000.00"
    M3 = "1.000,00"

class PropertyEnum(enum.Enum):
    NORMAL = 'normal'
    RENTED = "rented"

class DateDisplayEnum(str,enum.Enum):
    M1 = "YYYY/MM/DD"
    M2 = "YY/MM/DD"
    M3 = "YYYY-MM-DD"
    M4 = "YY-MM-DD"
    M5 = "MM/DD/YYYY"
    M6 = "MM/DD/YY"
    M7 = "MM-DD-YYYY"
    M8 = "MM-DD-YY"
    M9 = "MMM DD, YYYY"
    M10 = "MMM DD 'YY"

