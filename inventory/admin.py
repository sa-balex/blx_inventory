from django.contrib import admin, messages
from django.utils.html import format_html
from django.db.models import Q
from .models import Category, Bale, Supplier, Warehouse, Sale, BaleMovement, Customer
from .services import sell_bale
from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.action(description="Marcar como vendido")
def mark_as_sold(modeladmin, request, queryset):
    vendidos = 0
    ya_vendidos = 0
    errores = 0
    
    fardos_disponibles = queryset.filter(status=Bale.BaleStatus.AVAILABLE)
    ya_vendidos = queryset.filter(status=Bale.BaleStatus.SOLD).count()
    
    for bale in fardos_disponibles:
        try:
            sale = sell_bale(bale, sold_by=request.user)
            if sale:
                vendidos += 1
            else:
                errores += 1
        except Exception as e:
            errores += 1
            messages.error(request, f"Error al vender {bale.code}: {str(e)}")
    
    if vendidos:
        messages.success(request, f"{vendidos} fardo(s) marcado(s) como vendido(s)")
    
    if ya_vendidos:
        messages.warning(request, f"{ya_vendidos} fardo(s) ya estaba(n) vendido(s)")
    
    if errores:
        messages.error(request, f"{errores} fardo(s) no pudo(ieron) ser vendido(s)")


@admin.register(Bale)
class BaleAdmin(admin.ModelAdmin):
  list_display = (
    'code', 
    'name', 
    'category', 
    'status_badge', 
    'purchase_price', 
    'sale_price', 
    'show_profit',
    'sell_action',
    'is_active'
  )
  list_filter = ('status', 'category', 'is_active', 'created_at')
  search_fields = ('code', 'name', 'category__name')
  readonly_fields = ('code', 'created_at', 'updated_at', 'show_profit')
  actions = [mark_as_sold]
  
  fieldsets = (
      ('Información General', {
          'fields': ('code', 'name', 'category')
      }),
      ('Precios', {
          'fields': ('purchase_price', 'sale_price', 'show_profit')
      }),
      ('Estado', {
          'fields': ('status', 'is_active')
      }),
      ('Fechas', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      }),
  )
  
  def status_badge(self, obj):
      colors = {
          Bale.BaleStatus.AVAILABLE: '#28a745',
          Bale.BaleStatus.SOLD: '#dc3545',
          Bale.BaleStatus.RESERVED: '#ffc107',
      }
      color = colors.get(obj.status, '#6c757d')
      return format_html(
          '<span style="background-color: {}; color: white; padding: 3px 10px; '
          'border-radius: 3px; font-weight: bold;">{}</span>',
          color,
          obj.get_status_display()
      )
  status_badge.short_description = "Estado"
  
  def show_profit(self, obj):
     if obj.profit is None:
         return "-"
     return f"{obj.profit:.2f}"
  
  show_profit.short_description = "Ganancia"
  
  def get_queryset(self, request):
      qs = super().get_queryset(request)
      return qs.select_related('category')
  
  def sell_action(self, obj):
    if obj.status == Bale.BaleStatus.SOLD:
        return "-"
    url = reverse("admin:inventory_sale_add") + f"?bale={obj.id}"
    return mark_safe(f'<a class="button" href="{url}">Vender</a>')
  
  sell_action.short_description = "Acción"



@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('bale', 'customer',"amount", "sold_at", "sold_by")
    list_filter = ('sold_at', 'sold_by',)
    search_fields = ('bale__code', 'bale__name', 'customer__name',)
    # autocomplete_fields = ('bale','customer',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "bale":
          kwargs['queryset'] = Bale.objects.filter(status = Bale.BaleStatus.AVAILABLE)
      return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_changeform_initial_data(self, request):
      initial = super().get_changeform_initial_data(request)
      bale_id = request.GET.get("bale")
      if bale_id:
          initial["bale"] = bale_id
      return initial
    
    def save_model(self, request, obj, form, change):
      bale = obj.bale
      sell_bale(bale, sold_by=request.user)
      obj.amount = bale.sale_price
      obj.sold_by = request.user
      
      super().save_model(request, obj, form, change)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "document", "is_active")
    search_fields = ("name", "phone", "document")
    list_filter = ("is_active",)


admin.site.register(BaleMovement)