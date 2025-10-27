from django.db import models



class Category(models.Model):
  name = models.CharField("Nombre", max_length=100, unique=True)
  created_at = models.DateTimeField("Fecha de registro", auto_now_add=True)
  updated_at = models.DateTimeField("Última actualización", auto_now=True)

  class Meta:
    verbose_name = "Categoria"
    verbose_name_plural = "Categorias"
  
  def __str__(self):
    return self.name


class Supplier(models.Model):
  name = models.CharField("Nombre",max_length=200)
  phone = models.CharField("Celular", max_length=10)
  notes = models.TextField("Notas", blank=True)
  created_at = models.DateTimeField("Fecha de registro", auto_now_add=True)
  updated_at = models.DateTimeField("Última actualización", auto_now=True)

  class Meta:
    verbose_name = "Proveedor"
    verbose_name_plural = "Proveedores"

  def __str__(self):
    return self.name
  

def generate_bale_code():
  last = Bale.objects.order_by("id").last()
  next_id = 1 if not last else last.id + 1

  return f"F-{next_id:04d}"

  
class Bale(models.Model):
  class BaleStatus(models.TextChoices):
    AVAILABLE= 'AVAILABLE', 'Disponible'
    SOLD = 'SOLD', 'Vendido'
    RESERVED = 'RESERVED', 'Separado'

  code = models.CharField("Código",max_length=50, unique=True)
  name = models.CharField("Nombre", max_length=150)
  category = models.ForeignKey(Category, verbose_name="Categoría",on_delete = models.PROTECT)
  supplier = models.ForeignKey(Supplier, verbose_name="Proveedor", on_delete=models.SET_NULL, null=True, blank=True)

  purchase_price = models.DecimalField("Precio de compra", max_digits=10, decimal_places=2)
  sale_price = models.DecimalField("Precio de venta", max_digits=10, decimal_places=2, null=True, blank=True)

  status = models.CharField("Estado", max_length=10, choices=BaleStatus.choices, default=BaleStatus.AVAILABLE)
  created_at = models.DateTimeField("Fecha de registro", auto_now_add=True)
  updated_at = models.DateTimeField("Última actualización", auto_now=True)

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
  
  def __str__ (self):
    return f"{self.code} - ${self.name}"
