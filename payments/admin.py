from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'stripe_payment_intent_id', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['order__order_number', 'stripe_payment_intent_id']
    readonly_fields = ['stripe_payment_intent_id', 'stripe_client_secret', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'stripe_payment_intent_id', 'stripe_client_secret')
        }),
        ('Amount & Status', {
            'fields': ('amount', 'currency', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )