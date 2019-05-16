import factory
import pytest

from risk_maker.risk.config import FieldType
from risk_maker.risk.tests.factory import RiskFieldFactory, RiskFactory, RiskTypeFactory


@pytest.fixture
def risk_dict():
    return factory.build(dict, FACTORY_CLASS=RiskFactory)


@pytest.fixture
def risk_field_obj():
    return RiskFieldFactory()


@pytest.fixture
def required_risk_field_obj():
    return RiskFieldFactory(is_required=True)


@pytest.fixture
def risk_field_text_obj():
    return RiskFieldFactory(field_type=FieldType.TEXT)


@pytest.fixture
def risk_field_number_obj():
    return RiskFieldFactory(field_type=FieldType.NUMBER)


@pytest.fixture
def risk_field_date_obj():
    return RiskFieldFactory(field_type=FieldType.DATE)


@pytest.fixture
def risk_field_choice_obj():
    return RiskFieldFactory(field_type=FieldType.CHOICE)


@pytest.fixture
def multiple_risk_field_obj():
    risk_type = RiskTypeFactory()
    risk_fields = []
    for i in [FieldType.TEXT, FieldType.NUMBER, FieldType.DATE, FieldType.CHOICE]:
        risk_fields.append(RiskFieldFactory(field_type=i, risk_type=risk_type, is_required=True))
    return risk_fields
