from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='المستخدم',
    )
    session_key = models.CharField('مفتاح الجلسة', max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)

    class Meta:
        verbose_name = 'سلة'
        verbose_name_plural = 'السلات'

    def __str__(self):
        owner = self.user or f'زائر ({self.session_key})'
        return f'سلة {owner}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='السلة',
    )
    variant = models.ForeignKey(
        'catalog.ProductVariant',
        on_delete=models.CASCADE,
        verbose_name='خيار المنتج',
    )
    quantity = models.PositiveIntegerField('الكمية', default=1)

    class Meta:
        verbose_name = 'عنصر في السلة'
        verbose_name_plural = 'عناصر السلة'
        unique_together = ('cart', 'variant')

    def __str__(self):
        return f'{self.variant} × {self.quantity}'

    @property
    def subtotal(self):
        return self.variant.final_price * self.quantity