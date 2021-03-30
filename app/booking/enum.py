import enum

class PaymentEnum(str,enum.Enum):
    PARTIALLY_PAID = "partially_paid"

class SourceEnum(str,enum.Enum):
    AIRBNB = "airbnb"
    BEEHAZ = "beehaz"
