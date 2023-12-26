from django.contrib import admin

from .models import Payment,Product,Category,Cart,Order

admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)