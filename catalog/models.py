from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='التصنيف الأب',
    )
    name = models.CharField('الاسم', max_length=120)
    slug = models.SlugField('الرابط المختصر', unique=True, allow_unicode=True)
    is_active = models.BooleanField('نشط', default=True)

    class Meta:
        verbose_name = 'تصنيف'
        verbose_name_plural = 'التصنيفات'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='التصنيف',
    )
    name = models.CharField('الاسم', max_length=200)
    slug = models.SlugField('الرابط المختصر', unique=True, allow_unicode=True)
    description = models.TextField('الوصف', blank=True)
    price = models.DecimalField('السعر', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('نشط', default=True)
    created_at = models.DateTimeField('تاريخ الإضافة', auto_now_add=True)

    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name='المنتج',
    )
    sku = models.CharField('رمز المنتج (SKU)', max_length=60, unique=True)
    size = models.CharField('المقاس', max_length=30, blank=True)
    color = models.CharField('اللون', max_length=30, blank=True)
    price_override = models.DecimalField(
        'سعر خاص', max_digits=10, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField('المخزون', default=0)

    class Meta:
        verbose_name = 'خيار منتج'
        verbose_name_plural = 'خيارات المنتجات'

    @property
    def final_price(self):
        return self.price_override if self.price_override is not None else self.product.price

    def __str__(self):
        return f'{self.product.name} ({self.size} {self.color})'.strip()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='المنتج',
    )
    image = models.ImageField('الصورة', upload_to='products/')
    is_main = models.BooleanField('رئيسية', default=False)

    class Meta:
        verbose_name = 'صورة'
        verbose_name_plural = 'الصور'

    def __str__(self):
        return f'صورة {self.product.name}'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المنتج',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المستخدم',
    )
    rating = models.PositiveSmallIntegerField(
        'التقييم',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField('التعليق', blank=True)
    created_at = models.DateTimeField('تاريخ التقييم', auto_now_add=True)

    class Meta:
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقييمات'
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.product.name} - {self.rating}/5'