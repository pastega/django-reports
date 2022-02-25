from django.shortcuts import render
from django.views.generic import ListView, DetailView

import pandas as pd

from .models import Sale
from .forms import SalesSearchForm
from .utils import get_chart

from customers.models import Customer
from profiles.models import Profile
from reports.forms import ReportForm

def home_view(request):
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None

    if request.method == 'POST':

        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        sales_qs = Sale.objects.filter(created__gte=date_from).filter(created__lte=date_to)

        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())

            sales_df['customer_id'] = sales_df['customer_id'].apply(lambda id: Customer.objects.get(id=id))
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(lambda id: Profile.objects.get(id=id).user.username)
           
            sales_df['created'] = sales_df['created'].apply(lambda created: created.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda updated: updated.strftime('%Y-%m-%d')) 

            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'},
                            axis=1, inplace=True)

            positions_data = [
                {
                    'position_id': position.id, 
                    'product': position.product.name,
                    'quantity': position.quantity,
                    'price': position.price,
                    'sales_id': position.get_sales_id()
                } 
                for sale in sales_qs for position in sale.get_positions() 
            ]

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            chart = get_chart(chart_type, sales_df, results_by)

            # Convert dataframes to html, in order to display data
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
        else:
            no_data = 'No data available in this date range'

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'chart': chart,
        'no_data': no_data
    }

    return render(request, 'sales/home.html', context)

def sale_list_view(request):
    return render(request, 'sales/main.html', {'object_list': Sale.objects.all()})

def sale_detail_view(request, pk):
    return render(request, 'sales/detail.html', {'object': Sale.objects.get(pk=pk)})

# Same thing but with class-based views

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
