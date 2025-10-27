from django.db import transaction
from .models import Bale, Sale, Warehouse, BaleMovement

@transaction.atomic
def sell_bale(bale: Bale, amount=None, sold_by=None, notes = ""):
  if bale.status == Bale.BaleStatus.SOLD:
    return bale
  
  sale = Sale.objects.create(
    bale = bale,
    amount = amount if amount is not None else bale.sale_price,
    sold_by = sold_by,
    notes = notes,
  )

  BaleMovement.objects.create(
    bale=bale,
    type=BaleMovement.MovementType.SOLD,
    notes = notes
  )

  bale.status = Bale.BaleStatus.SOLD

  bale.is_active = False

  bale.save(update_fields=['status', 'is_active', 'updated_at'])

  return sale