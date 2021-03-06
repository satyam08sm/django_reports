from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from django.shortcuts import get_object_or_404
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id, get_chart

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def home_view(request):
    print(dir(request))
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    no_data = None

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        sale_qs = Sale.objects.filter(created__date__gte=date_from, created__date__lte=date_to)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(func=get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1,
                            inplace=True)

            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                        # works fine when position belongs to one sale but breaks if position belongs to multiple sales
                        # 'sales_id': sale.id,  # works even if the position belongs to multiple sales but in this case position belongs to only one sale
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            df = merged_df.groupby(results_by, as_index=False)['price'].agg('sum')

            chart = get_chart(chart_type, sales_df, results_by=results_by)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
        else:
            no_data = "No Data Available for selected values."
    context = {
        'search_form': search_form,
        'sales_df': sales_df,
        'position_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'report_form': report_form,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html', context)


class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'


# class SalesDetailView(DetailView):
#     model = Sale
#     template_name = 'sales/detail.html'

@login_required
def sales_detail_view(request, **kwargs):
    pk = kwargs.get('pk')
    obj = get_object_or_404(Sale, pk=pk)
    # or
    # obj = Sale.objects.get(pk=pk)

    return render(request, 'sales/detail.html', {'obj': obj})
