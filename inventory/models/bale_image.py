from django.db import models
from cloudinary.models import CloudinaryField
from .bale import Bale

class BaleImage(models.Model):
  bale = models.ForeignKey(Bale, on_delete=models.CASCADE, related_name="images")
  image = CloudinaryField("Imagen", folder="bales/images")
  uploaded_at = models.DateTimeField("Fecha de subida", auto_now_add=True)

  class Meta:
    verbose_name = "Imagen de fardo"
    verbose_name_plural = "Imagenes de fardos"

    def __str__(self):
      return f"Imagen de {self.bale.name}"