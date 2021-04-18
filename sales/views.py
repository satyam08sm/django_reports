from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from django.shortcuts import get_object_or_404
from .forms import SalesSearchForm


def home_view(request):
    form = SalesSearchForm(request.POST or None)
    hello = 'hello'
    context = {
        'hello': hello,
        'form': form
    }
    return render(request, 'sales/home.html', context)


class SalesListView(ListView):
    model = Sale
    template_name = 'sales/main.html'


# class SalesDetailView(DetailView):
#     model = Sale
#     template_name = 'sales/detail.html'

def sales_detail_view(request, **kwargs):
    pk = kwargs.get('pk')
    obj = get_object_or_404(Sale, pk=pk)
    # or
    # obj = Sale.objects.get(pk=pk)

    return render(request, 'sales/detail.html', {'obj': obj})
