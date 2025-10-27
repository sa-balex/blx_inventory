

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from inventory.models import Bale


@staff_member_required
def stock_dashboard(request):
  bales = Bale.objects.filter(is_active=True).order_by('-created_at')

  return render(request, "inventory/stock_dashboard.html", { "bales": bales});