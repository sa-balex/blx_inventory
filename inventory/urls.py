from django.urls import path
from .views.stock_dashboard import stock_dashboard

urlpatterns = [
    path("dashboard/", stock_dashboard, name="stock_dashboard")
]
