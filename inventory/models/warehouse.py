from django.db import models
from .base import SoftDeleteMixin

class Warehouse(SoftDeleteMixin):
  name = models.CharField("Nombre", max_length=100)
  address = models.CharField("Direccion", max_length= 200)

  class Meta:
    verbose_name = "Almacen"
    verbose_name_plural = "Almacenes"

  def __str__(self):
    return self.name
