from django.contrib import admin
from django.utils import timezone
from .models import Product, Order, OrderItem, State, City

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display    = ('name', 'price', 'stock', 'delivery_estimate_days', 'delivery_date')
    list_editable   = ('price', 'stock', 'delivery_estimate_days', 'delivery_date')
    search_fields   = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields          = (
        'user', 'price',
        ('delivery_status', 'delivered_on'),
        'address1', 'address2', 'city', 'state', 'pincode',
        'ordered_at', 'is_returned', 'return_reason',
    )
    readonly_fields = ('ordered_at',)
    list_display    = ('id', 'user', 'price', 'delivery_status', 'delivered_on', 'is_returned', 'ordered_at')
    list_editable   = ('delivery_status', 'delivered_on')
    list_filter     = ('delivery_status', 'is_returned')
    search_fields   = ('user__username', 'address1', 'city', 'state', 'pincode')
    inlines         = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display        = ('id', 'order', 'product', 'quantity')
    list_select_related = ('order', 'product')
    search_fields       = ('order__id', 'product__name')

admin.site.register(State)
admin.site.register(City)