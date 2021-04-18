from django.urls import path
from .views import (
    home_view,
    SalesListView,
    sales_detail_view
)

app_name = 'sales'

urlpatterns = [
    path('', home_view, name='home'),
    path('sales/', SalesListView.as_view(), name='list'),
    path('sales/<pk>', sales_detail_view, name='detail'),
]
