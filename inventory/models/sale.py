from django.db import models
from django.utils import timezone
from django.conf import settings
from . import Bale
from .customer import Customer
from .base import SoftDeleteMixin

class Sale(SoftDeleteMixin):
  bale = models.OneToOneField(Bale, verbose_name="Fardo", on_delete=models.PROTECT, related_name="sale")
  sold_at = models.DateTimeField("Fecha de venta", default=timezone.now)
  amount = models.DecimalField("Importe de venta", max_digits=10, decimal_places=2, null=True, blank=True)
  notes = models.TextField("Notas", blank=True)
  sold_by = models.ForeignKey(
    settings.AUTH_USER_MODEL, verbose_name="Vendido por",
    on_delete=models.SET_NULL, null=True, blank=True
  )
  customer = models.ForeignKey(Customer, verbose_name="Cliente", on_delete=models.PROTECT, null=True, blank=True)


  class Meta:
    verbose_name = "Venta"
    verbose_name_plural = "Ventas"

  def __str__(self):
    return f"Venta {self.bale.code} - {self.amount or self.bale.sale_price} "