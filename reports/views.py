from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa

from profiles.models import Profile
from django.http import JsonResponse, HttpResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView


class ReportListView(ListView):
    model = Report
    template_name = 'report/main.html'


def report_detail_view(request, pk):
    qs = Report.objects.get(id=pk)
    context = {
        'qs': qs,
    }
    return render(request, 'report/detail.html', context=context)


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
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
