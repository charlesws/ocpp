from ocpp2.charge_point import ChargePoint as cp
from ocpp2.v201 import call, call_result


class ChargePoint(cp):
    _call = call
    _call_result = call_result
    _ocpp_version = "2.0.1"
