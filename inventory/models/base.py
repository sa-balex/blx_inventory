from django.db import models

class SoftDeleteMixin(models.Model):
  is_active = models.BooleanField("Activo", default=True)
  created_at = models.DateTimeField("Fecha de registro", auto_now_add=True)
  updated_at = models.DateTimeField("Última actualización", auto_now=True)

  class Meta:
    abstract = True
