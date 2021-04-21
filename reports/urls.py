from django.urls import path
from .views import report_form_view, ReportListView, report_detail_view, render_pdf_view

app_name = 'reports'

urlpatterns = [
    path('', ReportListView.as_view(), name='main'),
    path('save/', report_form_view, name='create-report'),
    path('pdf/<pk>', render_pdf_view, name='pdf'),
    path('<pk>/', report_detail_view, name='detail'),
]
