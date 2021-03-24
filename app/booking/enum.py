import enum

class PaymentEnum(str,enum.Enum):
    INCOMPLETE = "incomplete"

class SourceEnum(str,enum.Enum):
    AIRBNB = "airbnb"
