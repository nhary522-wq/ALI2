from django.db import models


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = 'percent', 'نسبة مئوية'
        FIXED = 'fixed', 'مبلغ ثابت'

    code = models.CharField('الكود', max_length=40, unique=True)
    discount_type = models.CharField('نوع الخصم', max_length=10, choices=DiscountType.choices)
    value = models.DecimalField('القيمة', max_digits=10, decimal_places=2)
    min_order_total = models.DecimalField('الحد الأدنى للطلب', max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField('يبدأ في')
    valid_to = models.DateTimeField('ينتهي في')
    usage_limit = models.PositiveIntegerField('حد الاستخدام', null=True, blank=True)
    used_count = models.PositiveIntegerField('عدد مرات الاستخدام', default=0)
    is_active = models.BooleanField('نشط', default=True)

    class Meta:
        verbose_name = 'كوبون'
        verbose_name_plural = 'الكوبونات'

    def __str__(self):
        return self.code


class Promotion(models.Model):
    """عرض موسمي: خصم على منتجات أو تصنيفات معينة خلال فترة محددة."""

    class DiscountType(models.TextChoices):
        PERCENT = 'percent', 'نسبة مئوية'
        FIXED = 'fixed', 'مبلغ ثابت'

    title = models.CharField('عنوان العرض', max_length=150)
    description = models.TextField('الوصف', blank=True)
    discount_type = models.CharField('نوع الخصم', max_length=10, choices=DiscountType.choices)
    value = models.DecimalField('القيمة', max_digits=10, decimal_places=2)
    products = models.ManyToManyField(
        'catalog.Product',
        blank=True,
        related_name='promotions',
        verbose_name='المنتجات',
    )
    categories = models.ManyToManyField(
        'catalog.Category',
        blank=True,
        related_name='promotions',
        verbose_name='التصنيفات',
    )
    start_date = models.DateTimeField('يبدأ في')
    end_date = models.DateTimeField('ينتهي في')
    is_active = models.BooleanField('نشط', default=True)

    class Meta:
        verbose_name = 'عرض'
        verbose_name_plural = 'العروض'
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField('العنوان', max_length=150)
    image = models.ImageField('الصورة', upload_to='banners/')
    link = models.CharField('الرابط', max_length=300, blank=True)
    promotion = models.ForeignKey(
        Promotion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='banners',
        verbose_name='العرض المرتبط',
    )
    order = models.PositiveIntegerField('الترتيب', default=0)
    is_active = models.BooleanField('نشط', default=True)

    class Meta:
        verbose_name = 'بانر'
        verbose_name_plural = 'البانرات'
        ordering = ['order']

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField('العنوان', max_length=150)
    slug = models.SlugField('الرابط المختصر', unique=True, allow_unicode=True)
    content = models.TextField('المحتوى')
    is_published = models.BooleanField('منشورة', default=True)
    show_in_footer = models.BooleanField('تظهر في الفوتر', default=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)

    class Meta:
        verbose_name = 'صفحة'
        verbose_name_plural = 'الصفحات'
        ordering = ['title']

    def __str__(self):
        return self.title