from datetime import datetime

from risk_maker.risk.config import FieldType


def validate_date(val):
    try:
        datetime.strptime(val, '%Y-%m-%d')
    except ValueError:
        return False
    return True


def is_correct_field_type(field_type, val, choices):
    val_type = type(val)
    if field_type == FieldType.NUMBER and (val_type is int or val_type is float):
        return True
    if field_type == FieldType.TEXT and val_type is str:
        return True
    if field_type == FieldType.CHOICE and val_type is str and val in choices:
        return True
    if field_type == FieldType.DATE and val_type is str and validate_date(val):
        return True
    return False
