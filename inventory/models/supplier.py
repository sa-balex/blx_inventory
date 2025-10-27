from django.db import models
from .base import SoftDeleteMixin

class Supplier(SoftDeleteMixin):
  name = models.CharField("Nombre",max_length=200)
  phone = models.CharField("Celular", max_length=10)
  notes = models.TextField("Notas", blank=True)

  class Meta:
    verbose_name = "Proveedor"
    verbose_name_plural = "Proveedores"

  def __str__(self):
    return self.name
  