from django.db import models
from .base import SoftDeleteMixin

class Category(SoftDeleteMixin):
  name = models.CharField("Nombre", max_length=100, unique=True)

  class Meta:
    verbose_name = "Categoria"
    verbose_name_plural = "Categorias"
  
  def __str__(self):
    return self.name
