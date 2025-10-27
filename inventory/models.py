from django.db import models



class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)

  class Meta:
    verbose_name = "Categoria"
    verbose_name_plural = "Categorias"
  
  def __str__(self):
    return self.name



class Supplier(models.Model):
  name = models.CharField(max_length=200)
  phone = models.CharField(max_length=10)
  notes = models.TextField(blank=True)

  class Meta:
    verbose_name = "Proveedor"
    verbose_name_plural = "Proveedores"

  def __str__(self):
    return self.name
  
class Bale(models.Model):
  class BaleStatus(models.TextChoices):
    AVAILABLE= 'AVAILABLE', 'Disponible'
    SOLD = 'SOLD', 'Vendido'
    RESERVED = 'RESERVED', 'Separado'

  code = models.CharField(max_length=50, unique=True)
  name = models.CharField(max_length=150)
  category = models.ForeignKey(Category, on_delete = models.PROTECT)
  supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

  purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
  sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

  status = models.CharField(max_length=10, choices=BaleStatus.choices, default=BaleStatus.AVAILABLE)

  class Meta:
    verbose_name = "Fardo",
    verbose_name_plural = "Fardos"
