from django.test import TestCase

from cash_machine.models import Item
from cash_machine.serializers import ItemSerializer


class ItemSerializerTestCase(TestCase):
    def setUp(self):
        self.item_1 = Item.objects.create(title='test_1', price=100.0)
        self.item_2 = Item.objects.create(title='test_2', price=200.0)

    def test_ok(self):
        """Test case to Item serializer"""
        data = ItemSerializer([self.item_1, self.item_2], many=True).data
        print(data)
        expected_data = [{
            'id': self.item_1.id,
            'title': 'test_1',
            'price': 100.0
        },
        {
            'id': self.item_2.id,
            'title': 'test_2',
            'price': 200.0
        }]

        self.assertEqual(data, expected_data)
