from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta

class Product(models.Model):
    name                    = models.CharField(max_length=100)
    description             = models.TextField()
    image                   = models.ImageField(upload_to='products/')
    price                   = models.DecimalField(max_digits=10, decimal_places=2)
    stock                   = models.PositiveIntegerField(default=0)
    delivery_estimate_days  = models.PositiveIntegerField(
        default=3,
        help_text="Estimate in days from order date"
    )
    delivery_date           = models.DateField(
        null=True,
        blank=True,
        help_text="Optional fixed delivery date"
    )

    @property
    def estimated_delivery_date(self):
        """
        Returns either the admin-set delivery_date (if provided),
        otherwise falls back to today + delivery_estimate_days.
        """
        if self.delivery_date:
            return self.delivery_date
        return date.today() + timedelta(days=self.delivery_estimate_days)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Ordered', 'Ordered'),
        ('Processing', 'Processing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]

    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    price           = models.FloatField()
    address1        = models.CharField(max_length=255)
    address2        = models.CharField(max_length=255, blank=True)
    city            = models.CharField(max_length=100)
    state           = models.CharField(max_length=100)
    pincode         = models.CharField(max_length=10)
    ordered_at      = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Ordered')
    delivered_on    = models.DateField(null=True, blank=True)
    is_returned     = models.BooleanField(default=False)
    return_reason   = models.TextField(blank=True)

    def can_return(self):
        if self.delivered_on:
            return timezone.now().date() <= self.delivered_on + timedelta(days=7)
        return False

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.order.id}: {self.product.name} × {self.quantity}"


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name  = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name