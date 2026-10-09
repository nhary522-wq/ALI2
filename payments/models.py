from django.db import models


class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'قيد المعالجة'
        SUCCESS = 'success', 'ناجحة'
        FAILED = 'failed', 'فاشلة'
        REFUNDED = 'refunded', 'مستردة'

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='الطلب',
    )
    gateway = models.CharField('البوابة', max_length=40)  # moyasar, tap, ...
    gateway_ref = models.CharField('مرجع البوابة', max_length=120, blank=True, db_index=True)
    method = models.CharField('طريقة الدفع', max_length=40, blank=True)  # mada, visa, applepay
    amount = models.DecimalField('المبلغ', max_digits=10, decimal_places=2)
    currency = models.CharField('العملة', max_length=3, default='SAR')
    status = models.CharField('الحالة', max_length=20, choices=Status.choices, default=Status.PENDING)
    raw_response = models.JSONField('رد البوابة', default=dict, blank=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)

    class Meta:
        verbose_name = 'معاملة'
        verbose_name_plural = 'المعاملات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.gateway} - {self.amount} {self.currency}'