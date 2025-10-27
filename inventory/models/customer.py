from django.db import models
from .base import SoftDeleteMixin

class Customer(SoftDeleteMixin):
  name = models.CharField("Nombre del cliente", max_length=150)
  phone = models.CharField("Teléfono", max_length=20, null=True, blank=True)
  document = models.CharField("Documento (DNI/RUC)", max_length=20, null=True, blank=True)
  address = models.CharField("Dirección", max_length=255, null=True, blank=True)
  is_active = models.BooleanField("Activo", default=True)

  class Meta:
      verbose_name = "Cliente"
      verbose_name_plural = "Clientes"
      ordering = ["name"]

  def __str__(self):
      return self.name