from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from django.template.loader import get_template
from django.conf import settings

from xhtml2pdf import pisa

from profiles.models import Profile
from .utils import get_report_image
from .models import Report

class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'

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
