from django.contrib import admin
from .models import Product, category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['created_by', 'created_at']
    list_display = ['title', 'created_by', 'created_at']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif getattr(request.user, 'is_seller', False):
            return qs.filter(created_by=request.user)
        return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.created_by != request.user:
            return False
        return getattr(request.user, 'is_seller', False)

    def has_delete_permission(self, request, obj=None):

        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        # نفس منطق العرض
        if request.user.is_superuser:
            return True
        if obj is not None and obj.created_by != request.user:
            return False
        return getattr(request.user, 'is_seller', False)

    def has_add_permission(self, request):
        # بس البائعين أو الأدمن يقدروا يضيفوا منتج
        return request.user.is_superuser or getattr(request.user, 'is_seller', False)

    def save_model(self, request, obj, form, change):
        # تعيين المستخدم كمُنشئ/مُعدل
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)
admin.site.register(category)