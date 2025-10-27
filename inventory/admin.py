from django.contrib import admin
from .models import Category, Bale, Supplier

@admin.register(Bale)
class BaleAdmin(admin.ModelAdmin):
  list_display = ('code', 'name', 'category', 'status', 'purchase_price', 'sale_price')
  list_filter = ('status', 'category')
  search_fields = ('code', 'name')

admin.site.register(Category)
admin.site.register(Supplier)
