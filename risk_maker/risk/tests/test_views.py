import pytest
from django.urls import reverse
from faker import Faker

from risk_maker.risk.config import FieldType

fake = Faker()


class TestCreateRisk:

    @pytest.fixture
    def url(self):
        return reverse('risk-create')

    def test_empty_risk(self, client, db, url, risk_dict, risk_field_obj):
        risk_dict['risk_type'] = risk_field_obj.risk_type.id
        risk_dict['data'] = {}
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 201

    def test_required_field_missing(self, client, db, url, risk_dict, required_risk_field_obj):
        risk_dict['risk_type'] = required_risk_field_obj.risk_type.id
        risk_dict['data'] = {}
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 400
        assert response.json()[required_risk_field_obj.name] == ['This field may not be null.']

    @pytest.mark.parametrize('val', [fake.word(), fake.sentence(), fake.text()])
    def test_text_field(self, client, db, url, risk_dict, risk_field_text_obj, val):
        risk_dict['risk_type'] = risk_field_text_obj.risk_type.id
        risk_dict['data'] = {
            risk_field_text_obj.name: val
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 201
        assert response.json()['data'][risk_field_text_obj.name] == val

    @pytest.mark.parametrize('val', [fake.pyint(), fake.pyfloat()])
    def test_number_field(self, client, db, url, risk_dict, risk_field_number_obj, val):
        risk_dict['risk_type'] = risk_field_number_obj.risk_type.id
        risk_dict['data'] = {
            risk_field_number_obj.name: val
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 201
        assert response.json()['data'][risk_field_number_obj.name] == val

    def test_date_field(self, client, db, url, risk_dict, risk_field_date_obj):
        risk_dict['risk_type'] = risk_field_date_obj.risk_type.id
        val = fake.date()
        risk_dict['data'] = {
            risk_field_date_obj.name: val
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 201
        assert response.json()['data'][risk_field_date_obj.name] == val

    def test_choice_field(self, client, db, url, risk_dict, risk_field_choice_obj):
        risk_dict['risk_type'] = risk_field_choice_obj.risk_type.id
        val = fake.random_element(elements=risk_field_choice_obj.choices)
        risk_dict['data'] = {
            risk_field_choice_obj.name: val
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 201
        assert response.json()['data'][risk_field_choice_obj.name] == val

    def test_incorrect_text_field(self, client, db, url, risk_dict, risk_field_text_obj):
        risk_dict['risk_type'] = risk_field_text_obj.risk_type.id
        risk_dict['data'] = {
            risk_field_text_obj.name: fake.pyint()
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 400
        assert response.json()[risk_field_text_obj.name] == ['Please enter a valid Text']

    def test_incorrect_number_field(self, client, db, url, risk_dict, risk_field_number_obj):
        risk_dict['risk_type'] = risk_field_number_obj.risk_type.id
        risk_dict['data'] = {
            risk_field_number_obj.name: fake.word()
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 400
        assert response.json()[risk_field_number_obj.name] == ['Please enter a valid Number']

    @pytest.mark.parametrize('val', [fake.year(), fake.word(), fake.pyint(), fake.date_time()])
    def test_incorrect_date_field(self, client, db, url, risk_dict, risk_field_date_obj, val):
        risk_dict['risk_type'] = risk_field_date_obj.risk_type.id
        risk_dict['data'] = {
            risk_field_date_obj.name: val
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 400
        assert response.json()[risk_field_date_obj.name] == ['Please enter a valid Date']

    @pytest.mark.parametrize('val', [fake.pyint(), fake.word()])
    def test_incorrect_choice_field(self, client, db, url, risk_dict, risk_field_choice_obj, val):
        risk_dict['risk_type'] = risk_field_choice_obj.risk_type.id
        risk_dict['data'] = {
            risk_field_choice_obj.name: val
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 400
        assert response.json()[risk_field_choice_obj.name] == ['Please enter a valid Choice']

    def test_multiple_field_missing(self, client, db, url, risk_dict, multiple_risk_field_obj):
        risk_dict['risk_type'] = multiple_risk_field_obj[0].risk_type.id
        risk_dict['data'] = {}
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 400
        for i in [FieldType.TEXT, FieldType.NUMBER, FieldType.DATE, FieldType.CHOICE]:
            assert response.json()[multiple_risk_field_obj[i].name] == ['This field may not be null.']

    def test_multiple_field(self, client, db, url, risk_dict, multiple_risk_field_obj):
        risk_dict['risk_type'] = multiple_risk_field_obj[0].risk_type.id
        risk_dict['data'] = {
            multiple_risk_field_obj[0].name: fake.word(),
            multiple_risk_field_obj[1].name: fake.pyint(),
            multiple_risk_field_obj[2].name: fake.date(),
            multiple_risk_field_obj[3].name: fake.random_element(elements=multiple_risk_field_obj[3].choices)
        }
        response = client.post(url, risk_dict, content_type='application/json')
        assert response.status_code == 201
