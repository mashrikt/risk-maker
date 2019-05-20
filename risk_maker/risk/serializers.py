from rest_framework.serializers import ModelSerializer, ValidationError

from risk_maker.risk.config import FieldType
from risk_maker.risk.models import RiskField, RiskType, Risk
from risk_maker.risk.utils import is_correct_field_type


class RiskFieldSerializer(ModelSerializer):

    class Meta:
        model = RiskField
        fields = ('id', 'name', 'display_name', 'field_type', 'is_required', 'choices')


class RiskTypeSerializer(ModelSerializer):
    risk_fields = RiskFieldSerializer(many=True)

    class Meta:
        model = RiskType
        fields = ('id', 'name', 'risk_fields')


class RiskSerializer(ModelSerializer):

    class Meta:
        model = Risk
        fields = ('id', 'risk_type', 'name', 'data')

    def validate(self, attrs):
        risk_type = attrs.get('risk_type')
        data = attrs.get('data')
        risk_fields = risk_type.risk_fields.all()
        processed_data = {}
        error_message = {}
        for risk_field in risk_fields:
            name = risk_field.name
            val = data.get(name, None)
            field_type = risk_field.field_type
            val = int(val) if field_type == FieldType.NUMBER and type(val) == str and val.isdigit() else val
            if risk_field.is_required and val is None:
                error_message[name] = ['This field may not be null.']
            elif val and not is_correct_field_type(field_type, val, risk_field.choices):
                error_message[name] = f'Please enter a valid {risk_field.get_field_type_display()}'
            elif val is not None:
                processed_data[name] = val
        if error_message:
            raise ValidationError(error_message)
        attrs['data'] = processed_data
        return attrs
