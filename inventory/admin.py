from django.contrib import admin
from .models import Category, Bale, Supplier

@admin.register(Bale)
class BaleAdmin(admin.ModelAdmin):
  list_display = ('code', 'name', 'category', 'status', 'purchase_price', 'sale_price', 'show_profit')
  list_filter = ('status', 'category')
  search_fields = ('code', 'name')

  readonly_fields = ('code',)

  def show_profit(self, obj):
        if obj.profit is None:
            return "-"
        return f"{obj.profit:.2f}"
  
  show_profit.short_description = "Ganancia"

admin.site.register(Category)
admin.site.register(Supplier)
