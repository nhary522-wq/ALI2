from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'جديد'
        PAID = 'paid', 'مدفوع'
        SHIPPING = 'shipping', 'قيد الشحن'
        COMPLETED = 'completed', 'مكتمل'
        CANCELLED = 'cancelled', 'ملغي'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='العميل',
    )
    status = models.CharField('الحالة', max_length=20, choices=Status.choices, default=Status.NEW)
    coupon = models.ForeignKey(
        'promotions.Coupon',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='الكوبون',
    )

    # نسخة مجمّدة من بيانات الشحن وقت الطلب
    ship_name = models.CharField('اسم المستلم', max_length=150)
    ship_phone = models.CharField('جوال المستلم', max_length=20)
    ship_city = models.CharField('المدينة', max_length=100)
    ship_district = models.CharField('الحي', max_length=100, blank=True)
    ship_street = models.CharField('الشارع', max_length=200)
    ship_postal_code = models.CharField('الرمز البريدي', max_length=10, blank=True)

    subtotal = models.DecimalField('المجموع الفرعي', max_digits=10, decimal_places=2)
    discount = models.DecimalField('الخصم', max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField('رسوم الشحن', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('الإجمالي', max_digits=10, decimal_places=2)

    created_at = models.DateTimeField('تاريخ الطلب', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']

    def __str__(self):
        return f'طلب #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='الطلب',
    )
    variant = models.ForeignKey(
        'catalog.ProductVariant',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='خيار المنتج',
    )
    product_name = models.CharField('اسم المنتج', max_length=200)  # مجمّد
    variant_label = models.CharField('الخيار', max_length=100, blank=True)  # مجمّد
    unit_price = models.DecimalField('سعر الوحدة', max_digits=10, decimal_places=2)  # مجمّد
    quantity = models.PositiveIntegerField('الكمية')

    class Meta:
        verbose_name = 'عنصر في الطلب'
        verbose_name_plural = 'عناصر الطلب'

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'

    @property
    def subtotal(self):
        return self.unit_price * self.quantity