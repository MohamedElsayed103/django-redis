from django.core.management.base import BaseCommand
from core.models import Product
import random


class Command(BaseCommand):
    help = 'Populate database with sample products for caching demonstration'

    def handle(self, *args, **options):
        # Clear existing products
        Product.objects.all().delete()
        
        product_names = [
            'Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor',
            'Keyboard', 'Mouse', 'Webcam', 'Microphone', 'Speaker',
            'Router', 'SSD Drive', 'RAM Module', 'Graphics Card', 'Processor',
            'Motherboard', 'Power Supply', 'Case', 'Cooling Fan', 'USB Hub',
            'External HDD', 'Memory Card', 'Phone Case', 'Screen Protector', 'Charger',
            'HDMI Cable', 'USB Cable', 'Network Cable', 'Adapter', 'Docking Station'
        ]
        
        descriptions = [
            'High-quality product with excellent features',
            'Premium grade item for professional use',
            'Budget-friendly option with good performance',
            'Latest model with advanced technology',
            'Bestseller with great customer reviews',
            'Eco-friendly and sustainable choice',
            'Compact and portable design',
            'Heavy-duty for intensive use',
            'Sleek and modern appearance',
            'Value for money product'
        ]
        
        products_created = 0
        
        for name in product_names:
            Product.objects.create(
                name=name,
                description=random.choice(descriptions),
                price=round(random.uniform(10.0, 999.99), 2),
                stock=random.randint(0, 500)
            )
            products_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {products_created} products!')
        )
