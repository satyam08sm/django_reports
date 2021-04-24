from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa

from profiles.models import Profile
from django.http import JsonResponse, HttpResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, TemplateView
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer

import csv


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'report/main.html'


@login_required
def report_detail_view(request, pk):
    qs = Report.objects.get(id=pk)
    context = {
        'qs': qs,
    }
    return render(request, 'report/detail.html', context=context)


@login_required
def report_form_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        author = Profile.objects.get(user=request.user)

        img = get_report_image(image)

        Report.objects.create(name=name, remarks=remarks, author=author, image=img)

        return JsonResponse({'msg': 'Report created'})
    return JsonResponse({'msg': 'Error Occurred'})


@login_required
def render_pdf_view(request, pk):
    template_path = 'report/pdf.html'
    context = {'pdf_object': get_object_or_404(Report, pk=pk)}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'report/from_file.html'


@login_required
def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    # print(row)
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    created = parse_date(row[5])

                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None
                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=created)

                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj,
                                                                 salesman=salesman_obj, created=created)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
                return JsonResponse({'file_upload': True})
        return JsonResponse({'file_upload': False})
    return HttpResponse()
