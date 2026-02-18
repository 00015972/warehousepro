from django.test import TestCase
from django.contrib.auth import get_user_model

from inventory.models import Category, Product
from stock.models import StockMovement


User = get_user_model()


class StockCalculationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass12345")
        self.cat = Category.objects.create(name="TestCat")
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST-001",
            unit_price=100,
            reorder_level=5,
            category=self.cat,
        )

    def test_stock_starts_zero(self):
        self.assertEqual(self.product.current_stock(), 0)

    def test_in_movement_increases_stock(self):
        StockMovement.objects.create(
            product=self.product,
            movement_type=StockMovement.MovementType.IN,
            reference_type=StockMovement.ReferenceType.MANUAL,
            reference_id="",
            quantity=10,
            note="",
            created_by=self.user,
        )
        self.assertEqual(self.product.current_stock(), 10)

    def test_out_movement_decreases_stock(self):
        StockMovement.objects.create(
            product=self.product,
            movement_type=StockMovement.MovementType.IN,
            reference_type=StockMovement.ReferenceType.MANUAL,
            reference_id="",
            quantity=10,
            note="",
            created_by=self.user,
        )
        StockMovement.objects.create(
            product=self.product,
            movement_type=StockMovement.MovementType.OUT,
            reference_type=StockMovement.ReferenceType.MANUAL,
            reference_id="",
            quantity=3,
            note="",
            created_by=self.user,
        )
        self.assertEqual(self.product.current_stock(), 7)

    def test_low_stock_condition(self):
        StockMovement.objects.create(
            product=self.product,
            movement_type=StockMovement.MovementType.IN,
            reference_type=StockMovement.ReferenceType.MANUAL,
            reference_id="",
            quantity=5,
            note="",
            created_by=self.user,
        )
        self.assertTrue(self.product.current_stock() <= self.product.reorder_level)

    def test_multiple_movements_aggregate_correctly(self):
        StockMovement.objects.create(
            product=self.product, movement_type="IN",
            reference_type="MANUAL", reference_id="",
            quantity=8, note="", created_by=self.user,
        )
        StockMovement.objects.create(
            product=self.product, movement_type="IN",
            reference_type="MANUAL", reference_id="",
            quantity=2, note="", created_by=self.user,
        )
        StockMovement.objects.create(
            product=self.product, movement_type="OUT",
            reference_type="MANUAL", reference_id="",
            quantity=4, note="", created_by=self.user,
        )
        self.assertEqual(self.product.current_stock(), 6)
