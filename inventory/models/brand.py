from django.db import models
from .base import SoftDeleteMixin

class Brand(SoftDeleteMixin):
  name = models.CharField("Nombre", max_length=200)

  class Meta:
    verbose_name = "Marca"
    verbose_name_plural = "Marcas"

  def __str__(self):
    return self.name