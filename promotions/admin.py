from django.contrib import admin

from .models import Coupon, Promotion, Banner, Page


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'value', 'valid_from', 'valid_to', 'used_count', 'is_active')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_type', 'value', 'start_date', 'end_date', 'is_active')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('title',)
    filter_horizontal = ('products', 'categories')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'promotion', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_footer')
    list_filter = ('is_published', 'show_in_footer')
    prepopulated_fields = {'slug': ('title',)}