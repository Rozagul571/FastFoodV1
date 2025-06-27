from decimal import Decimal
from django.db.models import Sum, F
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(user_location, rest_location):
    if user_location and rest_location:
        lat1, lon1 = radians(user_location.y), radians(user_location.x)
        lat2, lon2 = radians(rest_location.y), radians(rest_location.x)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371 * c
        return round(distance, 3) if distance > 0 else None
    return None

def calculate_totals(order):
    result = order.order_items.aggregate(
        total_quantity=Sum('quantity'),
        total_price=Sum(F('price') * F('quantity'))
    )
    quantity = result['total_quantity'] or 0
    items_price = result['total_price'] or Decimal('0.00')
    delivery_fee = Decimal(str((order.distance_km or 0) * 5000)).quantize(Decimal('0.01'))
    total = items_price + delivery_fee
    return quantity, items_price, total, delivery_fee

def estimate_delivery(order):
    result = order.order_items.aggregate(total_quantity=Sum('quantity'))
    quantity = result['total_quantity'] or 0
    preparation = quantity * 75
    delivery = max(300, float(order.distance_km or 0) * 180)
    total_time = preparation + delivery
    return int(total_time)  # Faqat total_time qaytariladi