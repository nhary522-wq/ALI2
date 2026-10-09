from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'عميل'
        STORE_MANAGER = 'manager', 'مدير متجر'

    phone = models.CharField('رقم الجوال', max_length=20, blank=True)
    role = models.CharField('الدور', max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    class Meta(AbstractUser.Meta):
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمون'

    def __str__(self):
        return self.get_full_name() or self.username


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='المستخدم',
    )
    full_name = models.CharField('الاسم الكامل', max_length=150)
    phone = models.CharField('الجوال', max_length=20)
    city = models.CharField('المدينة', max_length=100)
    district = models.CharField('الحي', max_length=100, blank=True)
    street = models.CharField('الشارع', max_length=200)
    building_no = models.CharField('رقم المبنى', max_length=20, blank=True)
    postal_code = models.CharField('الرمز البريدي', max_length=10, blank=True)
    is_default = models.BooleanField('افتراضي', default=False)
    created_at = models.DateTimeField('تاريخ الإضافة', auto_now_add=True)

    class Meta:
        verbose_name = 'عنوان'
        verbose_name_plural = 'العناوين'

    def __str__(self):
        return f'{self.full_name} - {self.city}'