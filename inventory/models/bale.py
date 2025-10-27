from django.db import models
from .category import Category
from .supplier import Supplier
from .warehouse import Warehouse
from .brand import Brand
from .base import SoftDeleteMixin

def generate_bale_code():
  last = Bale.objects.order_by("id").last()
  next_id = 1 if not last else last.id + 1

  return f"F-{next_id:04d}"

class Bale(SoftDeleteMixin):
  class BaleStatus(models.TextChoices):
    AVAILABLE= 'AVAILABLE', 'Disponible'
    SOLD = 'SOLD', 'Vendido'
    RESERVED = 'RESERVED', 'Separado'

  code = models.CharField("Código",max_length=50, unique=True)
  name = models.CharField("Nombre", max_length=150)
  brand = models.ForeignKey(Brand, verbose_name="Marca", on_delete=models.PROTECT, null=True, blank=True)
  category = models.ForeignKey(Category, verbose_name="Categoría",on_delete = models.PROTECT)
  supplier = models.ForeignKey(Supplier, verbose_name="Proveedor", on_delete=models.SET_NULL, null=True, blank=True)
  warehouse = models.ForeignKey(Warehouse, verbose_name="Almacen", on_delete=models.SET_NULL, null=True, blank=True)

  purchase_price = models.DecimalField("Precio de compra", max_digits=10, decimal_places=2)
  sale_price = models.DecimalField("Precio de venta", max_digits=10, decimal_places=2, null=True, blank=True)

  status = models.CharField("Estado", max_length=10, choices=BaleStatus.choices, default=BaleStatus.AVAILABLE)



  class Meta:
    verbose_name = "Fardo",
    verbose_name_plural = "Fardos"
    ordering = ["-created_at"]
  
  def save(self, *args, **kwargs):
    if not self.code:
      self.code = generate_bale_code()
    super().save(*args, **kwargs)

  @property
  def profit(self):
    if self.sale_price:
      return self.sale_price - self.purchase_price
    return None
  
  @property
  def is_sold(self):
    return self.status == self.BaleStatus.SOLD or hasattr(self, "sale")
  
  def __str__ (self):
    return f"{self.code} - ${self.name}"
