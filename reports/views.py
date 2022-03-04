from math import prod
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.template.loader import get_template
from django.conf import settings
from django.utils.dateparse import parse_date

from xhtml2pdf import pisa
import csv

from profiles.models import Profile
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer

from .utils import get_report_image
from .models import Report

class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'
    
def csv_upload_view(request):
    
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        
        if created:
            obj.csv_file = csv_file
            obj.save()
            
            with open(obj.csv_file.path, 'r') as file:
                reader = csv.reader(file)
                reader.__next__()
                for row in reader:
                    data = "".join(row)
                    data = data.split(';')
                    data.pop()

                    transaction_id = data[1]
                    product = data[2]
                    quantity = int(data[3])
                    customer = data[4]
                    date = parse_date(data[5])

                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None
                        
                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)
                        
                        sale_obj = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, 
                                                            salesman=salesman_obj, created=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()  
                return JsonResponse({'ex': False})
        else:        
            return JsonResponse({'ex': True})        
                            
    return HttpResponse()

def create_report_view(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = get_report_image(request.POST.get('image'))
        author = Profile.objects.get(user=request.user)

        Report.objects.create(name=name, remarks=remarks, image=image, author=author)

        return JsonResponse({'message': 'sent'})
    return JsonResponse({})

def render_pdf_view(request, pk):
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    
    response = HttpResponse(content_type='application/pdf')
    # Setting attachment; will download the file
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
   
    template = get_template('reports/pdf.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
