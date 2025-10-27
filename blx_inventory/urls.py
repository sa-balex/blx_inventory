
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "BLX Inventory - Panel de control"
admin.site.site_title = "BLX Inventory"

admin.site.index_title = "Gestion de fardos"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls'))
]
