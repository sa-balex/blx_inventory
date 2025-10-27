from django.db import models
from .base import SoftDeleteMixin
from .bale import Bale
from .warehouse import Warehouse


class BaleMovement(SoftDeleteMixin):
    class MovementType(models.TextChoices):
        RECEIVED = "RECEIVED", "Recepción"
        RESERVED = "RESERVED", "Separado"
        SOLD     = "SOLD",     "Vendido"
        TRANSFER = "TRANSFER", "Traslado"

    bale = models.ForeignKey(Bale, on_delete=models.CASCADE, related_name="movements")
    type = models.CharField("Tipo", max_length=20, choices=MovementType.choices)
    from_warehouse = models.ForeignKey(Warehouse, related_name="+",
                                       on_delete=models.SET_NULL, null=True, blank=True)
    to_warehouse   = models.ForeignKey(Warehouse, related_name="+",
                                       on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField("Notas", blank=True)