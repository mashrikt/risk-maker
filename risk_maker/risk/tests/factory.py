import factory
import factory.fuzzy
from faker import Faker

from risk_maker.risk.config import FieldType
from risk_maker.risk.models import RiskField, RiskType, Risk

fake = Faker()


class RiskTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = RiskType

    name = factory.Faker('word')


class RiskFieldFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = RiskField

    risk_type = factory.SubFactory(RiskTypeFactory)
    name = factory.Faker('word')
    display_name = factory.Faker('word')
    field_type = factory.fuzzy.FuzzyChoice([FieldType.TEXT, FieldType.NUMBER, FieldType.DATE, FieldType.CHOICE])

    @factory.lazy_attribute
    def choices(self):
        if self.field_type == FieldType.CHOICE:
            return fake.words()
        return


class RiskFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Risk

    name = factory.Faker('word')
