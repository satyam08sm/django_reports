from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from django.shortcuts import get_object_or_404
from .forms import SalesSearchForm
import pandas as pd


def home_view(request):
    sales_df = None
    positions_df = None
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sale_qs = Sale.objects.filter(created__date__gte=date_from, created__date__lte=date_to)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df = sales_df.to_html()

            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sale_id': pos.get_sales_id(),  # works fine when position belongs to one sale but breaks if position belongs to multiple sales
                        # 'sale_id': sale.id,  # works even if the position belongs to multiple sales but in this case position belongs to only one sale
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data).to_html()
        else:
            print("No data")
    context = {
        'form': form,
        'sales_df': sales_df,
        'position_df': positions_df,
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
