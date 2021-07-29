from django.test import TestCase
from ..management.commands.fetchdeals import make_records
from ..models import Deal
from .deals_data import mock_data

class MakeRecords(TestCase):
    def test_creates_deals_records(self):
        deals_data = mock_data

        make_records(deals_data=deals_data)

        self.assertEqual(Deal.objects.count(), 16)
        
        for deal in deals_data:
            try:
                recorded_deal = Deal.objects.get(title=deal['title'])
            except:
                self.fail('Deal not recorded')

    def test_updates_deals_records(self):
        deals_data = mock_data

        make_records(deals_data=deals_data)

        self.assertEqual(Deal.objects.count(), 16)

        changed_deal = mock_data[7]
        changed_deal['salePrice'] = '0.1'

        make_records([changed_deal])

        self.assertEqual(Deal.objects.count(), 16)

        recorded_changed_deal = Deal.objects.get(title=changed_deal['title'])
        
        self.assertEqual(recorded_changed_deal.dealID, mock_data[7]['dealID'])
        self.assertEqual(recorded_changed_deal.salePrice, 0.1)
    
