from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'gateway', 'method', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('gateway', 'method', 'status')
    search_fields = ('gateway_ref', 'order__id')
    readonly_fields = ('raw_response', 'created_at', 'updated_at')