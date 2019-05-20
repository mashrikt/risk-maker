from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

from risk_maker.risk.config import FieldType


class RiskType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class RiskField(models.Model):
    risk_type = models.ForeignKey(RiskType, on_delete=models.PROTECT, related_name='risk_fields')
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    field_type = models.PositiveSmallIntegerField(choices=FieldType.CHOICES)
    is_required = models.BooleanField(default=False)
    choices = ArrayField(models.CharField(max_length=10, blank=True), blank=True, null=True)

    def __str__(self):
        return f'{self.name}-{self.risk_type}'


class Risk(models.Model):
    risk_type = models.ForeignKey(RiskType, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    data = JSONField()

    def __str__(self):
        return f'{self.name}'
