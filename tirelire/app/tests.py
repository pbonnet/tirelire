from datetime import datetime, timedelta
from decimal import Decimal

from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from app.models import Cash, MoneyBox, MoneyBoxContent


class MoneyBoxRetrieveApiTestCase(APITestCase):
    def setUp(self):
        self.moneybox = baker.make(MoneyBox, name='Moneybox test')

    def get_url(self, moneybox_id: int) -> str:
        return reverse('api:moneyboxes-detail', args=(moneybox_id,))

    def test_get_moneybox(self):
        response = self.client.get(self.get_url(self.moneybox.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.moneybox.id)
        self.assertEqual(response.data['name'], 'Moneybox test')
        self.assertTrue(response.data['created_at'])
        self.assertTrue(response.data['updated_at'])
        self.assertFalse(response.data['broken'])

    def test_get_moneybox_not_found(self):
        response = self.client.get(self.get_url(111111))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')


class MoneyBoxListTestCase(APITestCase):

    def get_url(self) -> str:
        return reverse('api:moneyboxes-list')

    def setUp(self):
        self.moneyboxes = [
            baker.make(MoneyBox, name=f'Moneybox test {x}')
            for x in range(1, 11)
        ]
        # Overwriting created_at to have a list from least recent to most recent moneybox
        for idx, moneybox in enumerate(self.moneyboxes):
            moneybox.created_at = datetime(2023, 1, 1) + timedelta(days=idx)

    def test_get_moneyboxes(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)
        # Reversing list because the endpoint should return by default from most recent to least recent moneybox
        self.moneyboxes.reverse()
        for idx, moneybox in enumerate(self.moneyboxes):
            self.assertEqual(moneybox.id, response.data[idx]['id'])


class MoneyBoxCreateTestCase(APITestCase):

    def get_url(self) -> str:
        return reverse('api:moneyboxes-list')

    def test_create_moneybox(self):
        payload = {'name': 'Moneybox test'}
        response = self.client.post(self.get_url(), payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Moneybox test')
        self.assertTrue(response.data['id'])
        self.assertTrue(response.data['created_at'])
        self.assertTrue(response.data['updated_at'])
        self.assertFalse(response.data['broken'])

    def test_create_moneybox_missing_name(self):
        payload = {}
        response = self.client.post(self.get_url(), payload, format='json')
        self.assertEqual(response.data['name'], ['This field is required.'])


class MoneyBoxSaveTestCase(APITestCase):

    def setUp(self):
        self.moneybox = baker.make(MoneyBox, name='Moneybox test')
        self.payload = {
            'cashes': [
                {
                    'cash_type': 'bill',
                    'value': '100',
                    'amount': 2
                },
                {
                    'cash_type': 'coin',
                    'value': '2',
                    'amount': 1
                },
                {
                    'cash_type': 'coin',
                    'value': '0.2',
                    'amount': 5
                },
            ]
        }

    def get_url(self, moneybox_id: int) -> str:
        return reverse('api:moneyboxes-save', args=(moneybox_id,))

    def test_save_moneybox(self):
        response = self.client.post(self.get_url(self.moneybox.id), self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['wealth'], '203.00')
        self.assertEqual(len(response.data['cashes']), 3)
        self.assertEqual(response.data['cashes'][0]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][0]['value'], '0.20')
        self.assertEqual(response.data['cashes'][0]['amount'], 5)
        self.assertEqual(response.data['cashes'][1]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][1]['value'], '2.00')
        self.assertEqual(response.data['cashes'][1]['amount'], 1)
        self.assertEqual(response.data['cashes'][2]['cash_type'], 'bill')
        self.assertEqual(response.data['cashes'][2]['value'], '100.00')
        self.assertEqual(response.data['cashes'][2]['amount'], 2)

    def test_save_moneybox_with_existing_content(self):
        two_euro_coin = Cash.find_from_type_and_value(value=Decimal('2'), cash_type='coin')
        baker.make(MoneyBoxContent, money_box=self.moneybox, cash=two_euro_coin, amount=2)
        response = self.client.post(self.get_url(self.moneybox.id), self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['wealth'], '207.00')
        self.assertEqual(len(response.data['cashes']), 3)
        self.assertEqual(response.data['cashes'][0]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][0]['value'], '0.20')
        self.assertEqual(response.data['cashes'][0]['amount'], 5)
        self.assertEqual(response.data['cashes'][1]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][1]['value'], '2.00')
        self.assertEqual(response.data['cashes'][1]['amount'], 3)
        self.assertEqual(response.data['cashes'][2]['cash_type'], 'bill')
        self.assertEqual(response.data['cashes'][2]['value'], '100.00')
        self.assertEqual(response.data['cashes'][2]['amount'], 2)

    def test_save_moneybox_not_found(self):
        response = self.client.post(self.get_url(111), self.payload, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_save_moneybox_with_wrong_cash_value(self):
        self.payload['cashes'].append({
            'cash_type': 'coin',
            'value': '30',
            'amount': 1
        })
        response = self.client.post(self.get_url(self.moneybox.id), self.payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['cashes'][0], 'The coin with the value 30.00 does not exist.')

    def test_save_broken_moneybox(self):
        self.moneybox.broken = True
        self.moneybox.save()
        response = self.client.post(self.get_url(self.moneybox.id), self.payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'This money box is broken you cannot use it anymore.')


class MoneyBoxShakeTestCase(APITestCase):

    def get_url(self, moneybox_id: int) -> str:
        return reverse('api:moneyboxes-shake', args=(moneybox_id,))

    def setUp(self):
        self.moneybox = baker.make(MoneyBox, name='Moneybox test')
        baker.make(
            MoneyBoxContent,
            money_box=self.moneybox,
            cash=Cash.find_from_type_and_value(value=Decimal('100'), cash_type='bill'),
            amount=2
        )
        baker.make(
            MoneyBoxContent,
            money_box=self.moneybox,
            cash=Cash.find_from_type_and_value(value=Decimal('2'), cash_type='coin'),
            amount=1
        )
        baker.make(
            MoneyBoxContent,
            money_box=self.moneybox,
            cash=Cash.find_from_type_and_value(value=Decimal('0.2'), cash_type='coin'),
            amount=5
        )

    def test_shake_moneybox(self):
        response = self.client.get(self.get_url(self.moneybox.id))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['wealth'], '203.00')
        self.assertEqual(len(response.data['cashes']), 3)
        self.assertEqual(response.data['cashes'][0]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][0]['value'], '0.20')
        self.assertEqual(response.data['cashes'][0]['amount'], 5)
        self.assertEqual(response.data['cashes'][1]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][1]['value'], '2.00')
        self.assertEqual(response.data['cashes'][1]['amount'], 1)
        self.assertEqual(response.data['cashes'][2]['cash_type'], 'bill')
        self.assertEqual(response.data['cashes'][2]['value'], '100.00')
        self.assertEqual(response.data['cashes'][2]['amount'], 2)

    def test_save_moneybox_not_found(self):
        response = self.client.get(self.get_url(111))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_shake_broken_moneybox(self):
        self.moneybox.broken = True
        self.moneybox.save()
        response = self.client.get(self.get_url(self.moneybox.id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'This money box is broken you cannot use it anymore.')


class MoneyBoxBreakTestCase(APITestCase):

    def get_url(self, moneybox_id: int) -> str:
        return reverse('api:moneyboxes-break', args=(moneybox_id,))

    def setUp(self):
        self.moneybox = baker.make(MoneyBox, name='Moneybox test')
        baker.make(
            MoneyBoxContent,
            money_box=self.moneybox,
            cash=Cash.find_from_type_and_value(value=Decimal('100'), cash_type='bill'),
            amount=2
        )
        baker.make(
            MoneyBoxContent,
            money_box=self.moneybox,
            cash=Cash.find_from_type_and_value(value=Decimal('2'), cash_type='coin'),
            amount=1
        )
        baker.make(
            MoneyBoxContent,
            money_box=self.moneybox,
            cash=Cash.find_from_type_and_value(value=Decimal('0.2'), cash_type='coin'),
            amount=5
        )

    def test_break_moneybox(self):
        response = self.client.delete(self.get_url(self.moneybox.id))
        self.moneybox.refresh_from_db()
        # Check if money box is empty and marked as broken
        self.assertEqual(len(self.moneybox.moneyboxcontent_set.all()), 0)
        self.assertTrue(self.moneybox.broken)
        # Check the cashes returned
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['wealth'], '203.00')
        self.assertEqual(len(response.data['cashes']), 3)
        self.assertEqual(response.data['cashes'][0]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][0]['value'], '0.20')
        self.assertEqual(response.data['cashes'][0]['amount'], 5)
        self.assertEqual(response.data['cashes'][1]['cash_type'], 'coin')
        self.assertEqual(response.data['cashes'][1]['value'], '2.00')
        self.assertEqual(response.data['cashes'][1]['amount'], 1)
        self.assertEqual(response.data['cashes'][2]['cash_type'], 'bill')
        self.assertEqual(response.data['cashes'][2]['value'], '100.00')
        self.assertEqual(response.data['cashes'][2]['amount'], 2)

    def test_break_moneybox_not_found(self):
        response = self.client.delete(self.get_url(111))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_break_already_broken_moneybox(self):
        self.moneybox.broken = True
        self.moneybox.save()
        response = self.client.delete(self.get_url(self.moneybox.id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'This money box is broken you cannot use it anymore.')
