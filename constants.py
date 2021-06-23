SECRET_KEY = "SECRET_KEY"
class MS:
    MONTH = 2592000

class view_constants:
    SUCCESS = "success"
    BAD_REQUEST = "bad request"
    INTERNAL_ERROR = "internal error while processing request"
    NOT_AUTHENTICATED = "not authenticated"
    MAPPING_ERROR = "mapping error"
    USER_REGISTRATION_SUCCESSFUL = "user registration successful"
    USER_LOGGED_IN = "user logged in"
    TOKEN_NOT_VALID = "token rejected"
    NO_RECORD = "no record"
    MAIL_SENT = "mail sent"
    REQUEST_PARAMETERS_NOT_SUFFICIENT = "request criteria not met"
    DB_TRANSACTION_FAULT = "db transaction fault"

class payment_constants:
    OMS = {
        "id": "oms_fixed_v1",
        "cost": 2000,
        "currency": "usd",
        "description": "Get one month subscription",
        "quantity": 1,
        "payment_method_types": ["card"]
    }


SLACK_CHANNELS = {
    "server_exception": {
        "channel": "C025NFJ0YFL",
        "msg": "Exception encountered: {msg}"
    }
}